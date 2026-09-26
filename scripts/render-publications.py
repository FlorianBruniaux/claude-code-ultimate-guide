#!/usr/bin/env python3
"""Render the public EN/FR catalog with source hashes and resumable outputs.

Run from the repository root. Requires Quarto and its bundled Typst engine.
French full-guide exports require a current, reviewed translation registry.
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COLLECTIONS = ("guides", "whitepapers", "cards", "cheatsheets")
RUNTIME = {}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root, languages, collections, formats):
    jobs = []
    for language in languages:
        sources = []
        if "guides" in collections:
            suffix = "-fr" if language == "fr" else ""
            sources.append(("guides", root / f"whitepapers/guide-export{suffix}.qmd", "whitepaper-typst"))
        if "whitepapers" in collections:
            papers = sorted((root / f"whitepapers/{language}").glob("[0-9][0-9]-*.qmd"))
            prefixes = [path.name[:2] for path in papers]
            if sorted(prefixes) != [f"{number:02}" for number in range(13)]:
                raise ValueError(f"{language}: expected one whitepaper for each prefix 00 through 12")
            sources.extend(("whitepapers", path, "whitepaper-typst") for path in papers)
        if "cards" in collections:
            cards = sorted((root / f"whitepapers/recap-cards/{language}").glob("*.qmd"))
            if len(cards) != 58:
                raise ValueError(f"{language}: expected 58 recap cards, found {len(cards)}")
            sources.extend(("cards", path, "recap-card-typst") for path in cards)
        if "cheatsheets" in collections:
            sources.append(("cheatsheets", root / f"whitepapers/{language}/cheatsheet.qmd", "cheatsheet-typst"))
        for collection, source, pdf_format in sources:
            if not source.is_file():
                raise ValueError(f"Missing source: {source.relative_to(root)}")
            for extension in formats:
                if extension == "epub" and collection in ("cards", "cheatsheets"):
                    continue
                output = unicodedata.normalize("NFC", f"{collection}/{language}/{source.stem}.{extension}")
                jobs.append({"collection": collection, "language": language,
                             "source": source.relative_to(root).as_posix(), "output": output,
                             "format": pdf_format if extension == "pdf" else "epub"})
    outputs = [job["output"] for job in jobs]
    if len(outputs) != len(set(outputs)):
        raise ValueError("Publication output name collision")
    return jobs


def input_hashes(job):
    paths = {ROOT / job["source"], ROOT / "VERSION", Path(__file__).resolve()}
    pending = [ROOT / job["source"]]
    visited = set()
    while pending:
        source = pending.pop()
        if source in visited:
            continue
        visited.add(source)
        for name in re.findall(r"\{\{<\s*include\s+([^ >]+)\s*>\}\}", source.read_text()):
            included = (source.parent / name.strip('\"\'')).resolve()
            if not included.is_relative_to(ROOT):
                raise ValueError(f"Include outside repository: {job['source']}")
            if not included.is_file():
                raise ValueError(f"Missing include: {included.relative_to(ROOT)}")
            paths.add(included)
            pending.append(included)
    extension = {"guides": "whitepaper", "whitepapers": "whitepaper",
                 "cards": "recap-card", "cheatsheets": "cheatsheet"}[job["collection"]]
    # Quarto resolves the nearest matching extension in the source ancestry.
    # A whitepaper template edit must not invalidate unrelated recap cards.
    for parent in (ROOT / job["source"]).parents:
        candidate = parent / "_extensions" / extension
        if candidate.is_dir():
            paths.update(path for path in candidate.rglob("*") if path.is_file())
            break
        if parent == ROOT:
            raise ValueError(f"Missing extension {extension}: {job['source']}")
    for name in ("epub-styles.css", "nocite.lua", "fix-lists.lua"):
        paths.add(ROOT / "whitepapers" / name)
    if job["collection"] == "guides":
        suffix = ".fr" if job["language"] == "fr" else ""
        paths.add(ROOT / f"guide/ultimate-guide{suffix}.md")
        paths.add(ROOT / "scripts/preprocess-guide.py")
    return {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(paths)}


def render(job, destination, resume):
    output = destination / job["output"]
    output.parent.mkdir(parents=True, exist_ok=True)
    evidence = output.with_suffix(output.suffix + ".json")
    before = input_hashes(job)
    if resume and evidence.exists() and output.exists():
        previous = json.loads(evidence.read_text())
        if (previous.get("inputs") == before and previous.get("runtime") == RUNTIME
                and previous.get("sha256") == digest(output)):
            return previous
    source = ROOT / job["source"]
    # Different formats of the same source run in sequence to avoid Quarto
    # temporary-file collisions. Independent sources may render concurrently.
    process = subprocess.run(["quarto", "render", source.name, "--to", job["format"],
                              "-M", "from:markdown+lists_without_preceding_blankline"],
                             cwd=source.parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True)
    output.with_suffix(output.suffix + ".log").write_text(process.stdout)
    if process.returncode:
        raise RuntimeError(f"Render failed: {job['output']} (see its .log file)")
    if before != input_hashes(job):
        raise RuntimeError(f"Source changed during render: {job['source']}")
    generated = source.with_suffix(output.suffix)
    if not generated.is_file() or generated.stat().st_size == 0:
        raise RuntimeError(f"Missing output: {job['output']}")
    shutil.copy2(generated, output)
    record = {**job, "inputs": before, "runtime": RUNTIME,
              "sha256": digest(output), "bytes": output.stat().st_size}
    if output.suffix == ".pdf":
        if not output.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError(f"Invalid PDF header: {job['output']}")
        if shutil.which("pdfinfo"):
            info = subprocess.run(["pdfinfo", str(output)], check=True, capture_output=True, text=True).stdout
            pages = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
            if not pages or int(pages.group(1)) < 1:
                raise RuntimeError(f"Unreadable PDF: {job['output']}")
            record["pages"] = int(pages.group(1))
    evidence.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    return record


def main():
    global RUNTIME
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang", choices=("en", "fr", "all"), default="all")
    parser.add_argument("--collections", nargs="+", choices=COLLECTIONS, default=list(COLLECTIONS))
    parser.add_argument("--formats", nargs="+", choices=("pdf", "epub"), default=["pdf", "epub"])
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist/publications")
    parser.add_argument("--jobs", type=int, default=3)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--list", action="store_true", help="Print the inventory without rendering")
    args = parser.parse_args()
    languages = ("en", "fr") if args.lang == "all" else (args.lang,)
    jobs = inventory(ROOT, languages, args.collections, args.formats)
    if args.list:
        print(json.dumps(jobs, ensure_ascii=False, indent=2))
        return 0
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    if not shutil.which("quarto"):
        parser.error("Quarto is required")
    for name, command in (("quarto", ["quarto", "--version"]),
                          ("typst", ["quarto", "typst", "--version"])):
        version = subprocess.run(command, check=True, capture_output=True, text=True)
        RUNTIME[name] = (version.stdout + version.stderr).strip()
    RUNTIME["fonts"] = {}
    for directory in os.environ.get("TYPST_FONT_PATHS", "").split(os.pathsep):
        if directory:
            for font in sorted(Path(directory).rglob("*")):
                if font.is_file() and font.suffix.lower() in (".ttf", ".otf"):
                    RUNTIME["fonts"][font.name] = digest(font)
    if "guides" in args.collections:
        if "fr" in languages:
            subprocess.run([sys.executable, str(ROOT / "scripts/check-translations.py"),
                            "--check", "--require-current-maintained"], check=True)
        for language in languages:
            suffix = ".fr" if language == "fr" else ""
            content_suffix = "-fr" if language == "fr" else ""
            subprocess.run([sys.executable, str(ROOT / "scripts/preprocess-guide.py"),
                            "--input", str(ROOT / f"guide/ultimate-guide{suffix}.md"),
                            "--output", str(ROOT / f"whitepapers/guide-content{content_suffix}.md")], check=True)
    destination = args.output_dir.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    groups = {}
    for job in jobs:
        groups.setdefault(job["source"], []).append(job)
    records, failures = [], []

    def render_source(group):
        return [render(job, destination, args.resume) for job in group]

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        pending = {executor.submit(render_source, group): source for source, group in groups.items()}
        for future in concurrent.futures.as_completed(pending):
            try:
                result = future.result()
                records.extend(result)
                print(f"OK {pending[future]} ({len(result)} outputs)", flush=True)
            except Exception as error:
                failures.append(str(error))
                print(f"ERROR {error}", file=sys.stderr, flush=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    manifest = {"generated_at": datetime.now(timezone.utc).isoformat(), "source_commit": head,
                "guide_version": (ROOT / "VERSION").read_text().strip(), "runtime": RUNTIME,
                "expected_outputs": len(jobs),
                "outputs": sorted(records, key=lambda row: row["output"]), "failures": failures}
    (destination / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"Completed {len(records)}/{len(jobs)} outputs; {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
