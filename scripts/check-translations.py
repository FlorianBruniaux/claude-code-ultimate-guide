#!/usr/bin/env python3
"""Validate translation freshness and bilingual publication parity."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "machine-readable" / "translations.json"
VERSION_RE = re.compile(r"^\*\*Version\*\*\s*:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", re.MULTILINE)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PREFIX_RE = re.compile(r"^(\d{2})-")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def extract_guide_version(path: Path) -> str:
    match = VERSION_RE.search(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"No **Version** field found in {path}")
    return match.group(1)


def parse_front_matter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"Missing front matter in {path}")

    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return result
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        result[key.strip()] = value
    raise ValueError(f"Unterminated front matter in {path}")


def expected_sync_state(
    canonical_version: str,
    translation_version: str,
    *,
    canonical_sha256: str | None = None,
    translated_from_sha256: str | None = None,
    maintained: bool = False,
) -> str:
    if translation_version != canonical_version:
        return "stale"
    if maintained:
        if not canonical_sha256 or translated_from_sha256 != canonical_sha256:
            return "stale"
        return "current"
    return "version_match_unverified"


def run_git(repo_root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_git_lag(
    repo_root: Path,
    source_commit: str,
    source_path: str,
    target_commit: str = "HEAD",
) -> dict[str, int]:
    return {
        "canonical_guide_commits": int(
            run_git(
                repo_root,
                "rev-list",
                "--count",
                f"{source_commit}..{target_commit}",
                "--",
                source_path,
            )
        ),
        "canonical_repo_commits": int(
            run_git(repo_root, "rev-list", "--count", f"{source_commit}..{target_commit}")
        ),
    }


def validate_evidence_registry(registry: dict[str, Any], repo_root: Path) -> list[str]:
    """Validate source commits, hashes, attribution fields, and pinned lag offline."""
    errors: list[str] = []
    measured_at = registry.get("measured_at_commit")
    if not isinstance(measured_at, str) or not SHA_RE.fullmatch(measured_at):
        return ["measured_at_commit must be a 40-character lowercase Git SHA"]

    policy = registry.get("policy", {})
    priorities = policy.get("official_translation_priority")
    if policy.get("canonical_language") != "en":
        errors.append("policy.canonical_language must be en")
    if not isinstance(priorities, list) or not priorities or priorities[0] != "fr":
        errors.append("French must be the first official translation priority")

    try:
        run_git(repo_root, "merge-base", "--is-ancestor", measured_at, "HEAD")
    except subprocess.CalledProcessError:
        errors.append("measured_at_commit is not an ancestor of HEAD")

    canonical = registry.get("canonical", {})
    canonical_path = canonical.get("path")
    canonical_source = canonical.get("source", {})
    canonical_lag = canonical.get("known_lag", {})
    for field in ("language", "url", "maintainer", "status", "version", "coverage", "known_lag"):
        if field not in canonical:
            errors.append(f"canonical missing field {field}")
    if canonical.get("status") != "official":
        errors.append("canonical status must be official")
    if not isinstance(canonical_source, dict) or not canonical_source.get("commit"):
        errors.append("canonical source commit must be present")
    elif isinstance(canonical_path, str):
        latest_commit = run_git(repo_root, "log", "-1", "--format=%H", "--", canonical_path)
        if canonical_source.get("commit") != latest_commit:
            errors.append("canonical source commit is not the latest commit that changed the guide")
        if canonical_source.get("sha256") != canonical.get("sha256"):
            errors.append("canonical source hash differs from canonical sha256")
    if canonical_lag.get("status") != "current" or any(
        canonical_lag.get(key) != 0
        for key in ("canonical_guide_commits", "canonical_repo_commits")
    ):
        errors.append("canonical known lag must be current with zero commit lag")

    languages: set[str] = set()
    for translation in registry.get("translations", []):
        language = translation.get("language", "UNKNOWN")
        if language in languages:
            errors.append(f"duplicate translation language {language}")
        languages.add(language)
        for field in (
            "url",
            "maintainer",
            "status",
            "version",
            "last_checked_at",
            "coverage",
            "known_lag",
            "translated_from",
        ):
            if field not in translation:
                errors.append(f"{language} missing field {field}")

        kind = translation.get("kind")
        if kind == "community" and (
            translation.get("status") != "community" or translation.get("official") is not False
        ):
            errors.append(f"{language} community translation must remain unofficial")
        if kind == "maintained" and translation.get("status") != "official":
            errors.append(f"{language} maintained translation must have project status official")

        source = translation.get("translated_from", {})
        lag = translation.get("known_lag", {})
        source_commit = source.get("commit") if isinstance(source, dict) else None
        if source_commit is None:
            if source.get("commit_evidence") != "not_declared":
                errors.append(f"{language} unknown source commit must say not_declared")
            if lag.get("status") != "unknown" or any(
                lag.get(key) is not None
                for key in ("canonical_guide_commits", "canonical_repo_commits")
            ):
                errors.append(f"{language} unknown source commit requires unknown numeric lag")
            continue
        if not isinstance(source_commit, str) or not SHA_RE.fullmatch(source_commit):
            errors.append(f"{language} source commit must be a full lowercase Git SHA")
            continue
        try:
            run_git(repo_root, "merge-base", "--is-ancestor", source_commit, measured_at)
            source_bytes = subprocess.run(
                ["git", "show", f"{source_commit}:{canonical_path}"],
                cwd=repo_root,
                check=True,
                capture_output=True,
            ).stdout
            source_version = run_git(repo_root, "show", f"{source_commit}:VERSION")
        except subprocess.CalledProcessError:
            errors.append(f"{language} source commit or canonical source file is unavailable")
            continue

        observed_source_hash = sha256_bytes(source_bytes)
        if source.get("sha256") != observed_source_hash:
            errors.append(f"{language} recorded source hash drifted")
        if source.get("version", translation.get("version")) != source_version:
            errors.append(f"{language} source version differs from its source commit VERSION")
        observed_lag = compute_git_lag(repo_root, source_commit, canonical_path, measured_at)
        for key, value in observed_lag.items():
            if lag.get(key) != value:
                errors.append(
                    f"{language} {key} drifted: recorded {lag.get(key)}, observed {value}"
                )
        expected_status = (
            "current"
            if observed_lag["canonical_guide_commits"] == 0
            and observed_source_hash == canonical.get("sha256")
            and source_version == canonical.get("version")
            else "stale"
        )
        if lag.get("status") != expected_status:
            errors.append(
                f"{language} freshness drifted: recorded {lag.get('status')}, observed {expected_status}"
            )

        if kind == "maintained":
            artifact = translation.get("artifact", {})
            path = repo_root / translation["path"]
            if artifact.get("sha256") != sha256_file(path):
                errors.append(f"{language} artifact hash drifted")

    if "fr" not in languages:
        errors.append("the maintained French translation is missing")

    for index, artifact in enumerate(registry.get("localized_artifacts", [])):
        for field in (
            "kind",
            "languages",
            "url",
            "maintainer",
            "status",
            "version",
            "source_commit",
            "last_checked_at",
            "coverage",
            "known_lag",
        ):
            if field not in artifact:
                errors.append(f"localized_artifacts[{index}] missing field {field}")
    return errors


def numbered_qmd_files(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for path in sorted(root.glob("*.qmd")):
        match = PREFIX_RE.match(path.name)
        if not match:
            continue
        prefix = match.group(1)
        if prefix in result:
            raise ValueError(f"Duplicate public prefix {prefix} in {root}")
        result[prefix] = path
    return result


def check_paired_metadata(
    left: Path,
    right: Path,
    left_lang: str,
    right_lang: str,
    shared_fields: tuple[str, ...],
) -> list[str]:
    errors: list[str] = []
    left_meta = parse_front_matter(left)
    right_meta = parse_front_matter(right)

    if left_meta.get("lang") != left_lang:
        errors.append(f"{left}: expected lang {left_lang!r}, found {left_meta.get('lang')!r}")
    if right_meta.get("lang") != right_lang:
        errors.append(f"{right}: expected lang {right_lang!r}, found {right_meta.get('lang')!r}")

    for field in shared_fields:
        left_value = left_meta.get(field)
        right_value = right_meta.get(field)
        if not left_value or not right_value:
            errors.append(f"{left.name} / {right.name}: missing paired field {field!r}")
        elif left_value != right_value:
            errors.append(
                f"{left.name} / {right.name}: {field} differs "
                f"({left_value!r} != {right_value!r})"
            )
    return errors


def validate_publication_pairs(registry: dict[str, Any], repo_root: Path) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    stats = {"whitepapers": 0, "whitepaper_revision_differences": 0, "recap_cards": 0}
    publications = registry["paired_publications"]

    whitepapers = publications["whitepapers"]
    fr_whitepapers = numbered_qmd_files(repo_root / whitepapers["roots"]["fr"])
    en_whitepapers = numbered_qmd_files(repo_root / whitepapers["roots"]["en"])
    expected_prefixes = set(whitepapers["public_prefixes"])
    known_unpaired = whitepapers.get("known_unpaired_prefixes", {})

    for language, files in (("fr", fr_whitepapers), ("en", en_whitepapers)):
        missing = sorted(expected_prefixes - set(files))
        declared_unpaired = set(known_unpaired.get(language, []))
        extra = sorted(set(files) - expected_prefixes - declared_unpaired)
        absent_unpaired = sorted(declared_unpaired - set(files))
        if missing:
            errors.append(f"Whitepapers {language}: missing paired source prefixes {', '.join(missing)}")
        if extra:
            errors.append(f"Whitepapers {language}: undeclared source prefixes {', '.join(extra)}")
        if absent_unpaired:
            errors.append(
                f"Whitepapers {language}: declared unpaired prefixes are absent "
                f"{', '.join(absent_unpaired)}"
            )

    for prefix in sorted(expected_prefixes & set(fr_whitepapers) & set(en_whitepapers)):
        errors.extend(
            check_paired_metadata(
                fr_whitepapers[prefix],
                en_whitepapers[prefix],
                "fr",
                "en",
                ("version",),
            )
        )
        fr_meta = parse_front_matter(fr_whitepapers[prefix])
        en_meta = parse_front_matter(en_whitepapers[prefix])
        if fr_meta.get("wp-version") != en_meta.get("wp-version"):
            stats["whitepaper_revision_differences"] += 1
        stats["whitepapers"] += 1

    recap = publications["recap_cards"]
    fr_recap_root = repo_root / recap["roots"]["fr"]
    en_recap_root = repo_root / recap["roots"]["en"]
    fr_recap = {path.name: path for path in sorted(fr_recap_root.glob("*.qmd"))}
    en_recap = {path.name: path for path in sorted(en_recap_root.glob("*.qmd"))}

    missing_en = sorted(set(fr_recap) - set(en_recap))
    missing_fr = sorted(set(en_recap) - set(fr_recap))
    if missing_en:
        errors.append(f"Recap cards en: missing {', '.join(missing_en)}")
    if missing_fr:
        errors.append(f"Recap cards fr: missing {', '.join(missing_fr)}")

    for name in sorted(set(fr_recap) & set(en_recap)):
        errors.extend(
            check_paired_metadata(
                fr_recap[name],
                en_recap[name],
                "fr",
                "en",
                ("version", "guide-version"),
            )
        )
        stats["recap_cards"] += 1

    return errors, stats


def validate_registry(
    registry: dict[str, Any],
    repo_root: Path,
    require_current_maintained: bool,
) -> tuple[list[str], list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    states: list[str] = []
    stale_languages: list[str] = []

    errors.extend(validate_evidence_registry(registry, repo_root))

    root_version = (repo_root / "VERSION").read_text(encoding="utf-8").strip()
    canonical = registry["canonical"]
    canonical_path = repo_root / canonical["path"]
    canonical_version = extract_guide_version(canonical_path)
    canonical_hash = sha256_file(canonical_path)

    if canonical["version"] != root_version or canonical_version != root_version:
        errors.append(
            "Canonical version mismatch: "
            f"VERSION={root_version}, registry={canonical['version']}, guide={canonical_version}"
        )
    if canonical["sha256"] != canonical_hash:
        errors.append(
            f"Canonical SHA-256 mismatch: registry={canonical['sha256']}, file={canonical_hash}"
        )
    states.append(f"English {canonical_version}: CURRENT, canonical SHA-256 {canonical_hash[:12]}")

    for translation in registry["translations"]:
        language = translation["language"]
        kind = translation["kind"]
        for date_field in ("last_checked_at", "last_full_refresh_at", "last_upstream_sync_at"):
            value = translation.get(date_field)
            if value and not DATE_RE.match(value):
                errors.append(f"{language}: invalid {date_field} {value!r}")

        if kind == "maintained":
            path = repo_root / translation["path"]
            local_version = extract_guide_version(path)
            if translation["version"] != local_version:
                errors.append(
                    f"{language}: registry version {translation['version']} differs from file {local_version}"
                )
            translated_from = translation.get("translated_from", {})
            expected = expected_sync_state(
                canonical_version,
                local_version,
                canonical_sha256=canonical_hash,
                translated_from_sha256=translated_from.get("sha256"),
                maintained=True,
            )
            if require_current_maintained and expected != "current":
                errors.append(
                    f"{language}: maintained translation is {expected}; "
                    "regenerate it before publishing a translated full-guide export"
                )
        elif kind == "community":
            if translation.get("official") is not False:
                errors.append(f"{language}: community translation must declare official=false")
            if not translation.get("repository", "").startswith("https://github.com/"):
                errors.append(f"{language}: missing canonical GitHub repository URL")
            expected = expected_sync_state(canonical_version, translation["version"])
        else:
            errors.append(f"{language}: unsupported translation kind {kind!r}")
            continue

        if translation.get("sync_state") != expected:
            errors.append(
                f"{language}: declared sync_state {translation.get('sync_state')!r} "
                f"contradicts computed state {expected!r}"
            )
        if expected != "current":
            stale_languages.append(language)
        states.append(
            f"{translation['label']} {translation['version']}: {expected.upper()}, {kind}"
        )

    publication_errors, stats = validate_publication_pairs(registry, repo_root)
    errors.extend(publication_errors)
    return errors, states, stale_languages, stats


def git_source_commit(repo_root: Path, source_path: str, source_hash: str) -> str:
    try:
        committed = subprocess.run(
            ["git", "show", f"HEAD:{source_path}"],
            cwd=repo_root,
            check=True,
            capture_output=True,
        ).stdout
        if hashlib.sha256(committed).hexdigest() != source_hash:
            return "working-tree"
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "working-tree"


def update_local_registry(
    registry_path: Path,
    repo_root: Path,
    record_french_refresh: bool,
) -> dict[str, Any]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    root_version = (repo_root / "VERSION").read_text(encoding="utf-8").strip()
    canonical = registry["canonical"]
    canonical_path = repo_root / canonical["path"]
    canonical_hash = sha256_file(canonical_path)

    canonical["version"] = root_version
    canonical["sha256"] = canonical_hash
    registry["checked_at"] = today
    measured_at = run_git(repo_root, "rev-parse", "HEAD")
    registry["measured_at_commit"] = measured_at
    canonical["source"] = {
        "commit": run_git(repo_root, "log", "-1", "--format=%H", "--", canonical["path"]),
        "sha256": canonical_hash,
        "commit_evidence": "latest_commit_touching_canonical_guide",
    }
    canonical["known_lag"] = {
        "status": "current",
        "canonical_guide_commits": 0,
        "canonical_repo_commits": 0,
    }

    for translation in registry["translations"]:
        if translation["kind"] != "maintained":
            continue
        translation_path = repo_root / translation["path"]
        translation["version"] = extract_guide_version(translation_path)
        translation["last_checked_at"] = today
        if record_french_refresh and translation["language"] == "fr":
            translation["translated_from"] = {
                "version": root_version,
                "commit": git_source_commit(repo_root, canonical["path"], canonical_hash),
                "sha256": canonical_hash,
            }
            translation["last_full_refresh_at"] = today
            translation.setdefault("artifact", {})["sha256"] = sha256_file(translation_path)
        translation["sync_state"] = expected_sync_state(
            root_version,
            translation["version"],
            canonical_sha256=canonical_hash,
            translated_from_sha256=translation.get("translated_from", {}).get("sha256"),
            maintained=True,
        )
    for translation in registry["translations"]:
        source_commit = translation.get("translated_from", {}).get("commit")
        if source_commit and source_commit != "working-tree":
            observed_lag = compute_git_lag(
                repo_root,
                source_commit,
                canonical["path"],
                measured_at,
            )
            translation["known_lag"].update(observed_lag)
            translation["known_lag"]["status"] = "current" if (
                observed_lag["canonical_guide_commits"] == 0
                and translation.get("translated_from", {}).get("sha256") == canonical_hash
                and translation.get("translated_from", {}).get("version", translation["version"])
                == root_version
            ) else "stale"

    registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.add_argument("--update-local", action="store_true", help="refresh canonical and local file facts")
    parser.add_argument(
        "--record-french-refresh",
        action="store_true",
        help="bind the French guide to the current canonical source after a completed translation",
    )
    parser.add_argument(
        "--require-current-maintained",
        action="store_true",
        help="fail when a maintained full-guide translation is stale",
    )
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry_path = args.registry.resolve()
    repo_root = args.repo_root.resolve()

    if args.record_french_refresh and not args.update_local:
        print("ERROR: --record-french-refresh requires --update-local", file=sys.stderr)
        return 2

    try:
        if args.update_local:
            registry = update_local_registry(registry_path, repo_root, args.record_french_refresh)
            print(f"Updated {registry_path}")
        else:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))

        errors, states, stale_languages, stats = validate_registry(
            registry,
            repo_root,
            args.require_current_maintained,
        )
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("=== Translation Status ===")
    for state in states:
        print(f"- {state}")
    print(f"- Whitepaper pairs: {stats['whitepapers']}")
    print(
        "- Whitepaper pairs with language-specific revision numbers: "
        f"{stats['whitepaper_revision_differences']}"
    )
    print(f"- Recap-card pairs: {stats['recap_cards']}")

    if stale_languages:
        print(f"Declared non-current editions: {', '.join(stale_languages)}")

    if errors:
        print("\nTranslation check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Translation metadata and publication parity are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
