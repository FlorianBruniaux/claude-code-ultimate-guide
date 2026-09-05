#!/usr/bin/env python3
"""
Translate guide/ultimate-guide.md from English to French.

Output : guide/ultimate-guide.fr.md
Resume : .translation-cache/ (chunk files, auto-cleaned on success)
Model  : claude-sonnet-5
"""

import hashlib
import json
import subprocess
import sys
import time
import traceback
from pathlib import Path

import anthropic

MAX_RETRIES = 3
RETRY_BACKOFF = [5, 15, 30]  # seconds between retries

# ── Config ────────────────────────────────────────────────────────────────────
SOURCE = Path("guide/ultimate-guide.md")
OUTPUT = Path("guide/ultimate-guide.fr.md")
CACHE  = Path(".translation-cache")
MODEL  = "claude-sonnet-5"
CACHE_MANIFEST = CACHE / "manifest.json"

# Max lines before forcing a split at the next heading
MAX_LINES_H2  = 200
MAX_LINES_H3  = 450

SYSTEM = """\
You are a technical translator English → French for the Claude Code Ultimate Guide.

KEEP IN ENGLISH — do not translate:
- All code blocks and inline code (`…`, ```…```)
- Shell commands, CLI flags (--flag), environment variables
- File/path names: CLAUDE.md, settings.json, .claude/, etc.
- Proper nouns: Claude Code, Claude, Anthropic, GitHub, VS Code, Cursor
- Technical identifiers: hooks, skills, agents, MCP, API, slash commands,
  SubAgent, TaskCreate, HEREDOC, worktree, compact, ultrathink
- Markdown structural syntax: ##, **, *, >, |, ```, [ ], ( ), ---

TRANSLATE to French:
- All prose, section titles (## headings text), table cell text, list items,
  callout text, admonitions, descriptions, explanations
- Maintain technical, clear, direct tone — no marketing language

PRESERVE exactly:
- All blank lines and spacing
- All markdown formatting structure
- All URLs (translate anchor text if it is prose)

OUTPUT: translated markdown only — no preamble, no commentary, no code fences \
wrapping the whole output.\
"""


# ── Chunking ──────────────────────────────────────────────────────────────────

def make_chunks(text: str) -> list[str]:
    lines   = text.split("\n")
    chunks  = []
    current = []

    for line in lines:
        if line.startswith("## ") and len(current) > MAX_LINES_H2:
            chunks.append("\n".join(current))
            current = [line]
        elif line.startswith("### ") and len(current) > MAX_LINES_H3:
            chunks.append("\n".join(current))
            current = [line]
        else:
            current.append(line)

    if current:
        chunks.append("\n".join(current))

    return chunks


def source_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def expected_cache_manifest(content: str, chunks: list[str]) -> dict[str, object]:
    return {
        "schema_version": 1,
        "source": SOURCE.as_posix(),
        "source_sha256": source_sha256(content),
        "model": MODEL,
        "chunk_count": len(chunks),
        "max_lines_h2": MAX_LINES_H2,
        "max_lines_h3": MAX_LINES_H3,
    }


def prepare_cache(expected: dict[str, object]) -> None:
    CACHE.mkdir(exist_ok=True)
    chunk_files = sorted(CACHE.glob("chunk_*.md"))

    if CACHE_MANIFEST.exists():
        actual = json.loads(CACHE_MANIFEST.read_text(encoding="utf-8"))
        if actual != expected:
            raise RuntimeError(
                "Translation cache belongs to another source, model, or chunking configuration. "
                "Move or remove .translation-cache before starting a new translation."
            )
        return

    if chunk_files:
        raise RuntimeError(
            "Translation cache contains chunks but no manifest. "
            "Move or remove .translation-cache before resuming."
        )

    CACHE_MANIFEST.write_text(
        json.dumps(expected, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# ── Translation ───────────────────────────────────────────────────────────────

def translate_chunk(
    client: anthropic.Anthropic,
    chunk:  str,
    idx:    int,
    total:  int,
) -> str:
    words = len(chunk.split())
    min_expected_chars = max(200, words * 0.5)  # reject obvious meta-responses only

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"  [{idx:3d}/{total}] {words:4d} words … ", end="", flush=True)
        t0 = time.time()

        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=8000,
                system=SYSTEM,
                messages=[{"role": "user", "content": chunk}],
            )
            elapsed = time.time() - t0

            result = next(
                (b.text for b in resp.content if hasattr(b, "text") and b.type == "text"),
                None,
            )

            if result is None:
                raise ValueError(f"No text block in response (blocks: {[type(b).__name__ for b in resp.content]})")

            if len(result) < min_expected_chars:
                raise ValueError(f"Output too short ({len(result)} chars for {words} words — likely meta-response)")

            print(f"{elapsed:.1f}s")
            return result

        except KeyboardInterrupt:
            raise
        except Exception as exc:
            print(f"FAIL (attempt {attempt}/{MAX_RETRIES}): {exc}")
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF[attempt - 1]
                print(f"  Retrying in {wait}s…")
                time.sleep(wait)
            else:
                raise


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    print(f"Reading {SOURCE} …")
    content     = SOURCE.read_text(encoding="utf-8")
    total_words = len(content.split())
    chunks      = make_chunks(content)
    expected_manifest = expected_cache_manifest(content, chunks)

    try:
        prepare_cache(expected_manifest)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Cache error: {exc}")
        return 1

    client = anthropic.Anthropic()

    cost_est = (total_words * 1.3 / 1e6 * 3) + (total_words * 1.3 * 1.1 / 1e6 * 15)
    print(f"  {total_words:,} words  |  {len(chunks)} chunks  |  ~${cost_est:.2f} est.")
    print(f"  Model: {MODEL}\n")

    t_start = time.time()

    for i, chunk in enumerate(chunks, 1):
        chunk_file = CACHE / f"chunk_{i:04d}.md"

        if chunk_file.exists():
            print(f"  [{i:3d}/{len(chunks)}] cached — skip")
            continue

        try:
            result = translate_chunk(client, chunk, i, len(chunks))
            chunk_file.write_text(result, encoding="utf-8")
        except KeyboardInterrupt:
            print("\nInterrupted. Run again to resume from this chunk.")
            return 1
        except Exception as exc:
            print(f"\nError on chunk {i}:")
            traceback.print_exc()
            print("Run again to resume.")
            return 1

    # ── Assemble ──────────────────────────────────────────────────────────────
    cached = sorted(CACHE.glob("chunk_*.md"))

    if len(cached) != len(chunks):
        print(f"\nPartial: {len(cached)}/{len(chunks)} chunks done. Run again to continue.")
        return 1

    print(f"\nAssembling {len(cached)} chunks → {OUTPUT}")
    OUTPUT.write_text(
        "\n\n".join(f.read_text(encoding="utf-8") for f in cached),
        encoding="utf-8",
    )

    out_words = len(OUTPUT.read_text(encoding="utf-8").split())
    total_sec = time.time() - t_start
    print(f"Done! {out_words:,} words | {total_sec:.0f}s total")

    try:
        subprocess.run(
            [
                sys.executable,
                "scripts/check-translations.py",
                "--update-local",
                "--record-french-refresh",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"Translation completed, but status recording failed with exit code {exc.returncode}.")
        print("The cache was kept so the output can be inspected before retrying the status update.")
        return 1

    # Clean up cache
    for f in cached:
        f.unlink()
    CACHE_MANIFEST.unlink()
    CACHE.rmdir()

    return 0


if __name__ == "__main__":
    sys.exit(main())
