#!/usr/bin/env python3
"""Check the rendered EN/FR catalog before copying or publishing downloads.

Run from the repository root after scripts/render-publications.py.
Requires Poppler's pdfinfo and pdftotext. Geometry checks detect text outside
the page; visual review is still needed for overlap, spacing and readability.
"""

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pdf(path, row):
    info = subprocess.run(["pdfinfo", str(path)], check=True, capture_output=True, text=True)
    if "Encrypted:       yes" in info.stdout:
        raise ValueError("PDF is encrypted")
    result = subprocess.run(["pdftotext", "-bbox-layout", str(path), "-"],
                            check=True, capture_output=True)
    document = ET.fromstring(result.stdout)
    pages = document.findall(".//{*}page")
    if len(pages) != row.get("pages"):
        raise ValueError("page count differs from build evidence")
    if row["collection"] == "cards" and len(pages) != 1:
        raise ValueError(f"recap card must fit one page, found {len(pages)}")
    words = []
    outside = []
    for number, page in enumerate(pages, 1):
        width, height = float(page.attrib["width"]), float(page.attrib["height"])
        for word in page.findall(".//{*}word"):
            text = "".join(word.itertext())
            words.append(text)
            box = {key: float(word.attrib[key]) for key in ("xMin", "yMin", "xMax", "yMax")}
            if (box["xMin"] < -0.5 or box["yMin"] < -0.5
                    or box["xMax"] > width + 0.5 or box["yMax"] > height + 0.5):
                outside.append({"page": number, "text": text[:80], "box": box})
    if sum(len(word) for word in words) < 100:
        raise ValueError("PDF has too little extractable text")
    if outside:
        raise ValueError(f"text outside page: {outside[:5]}")
    return {"pages": len(pages), "words": len(words), "outside_page_words": 0}


def check_epub(path, row):
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"corrupt ZIP member: {bad}")
        if archive.read("mimetype") != b"application/epub+zip":
            raise ValueError("invalid EPUB MIME type")
        first = archive.infolist()[0]
        if first.filename != "mimetype" or first.compress_type != zipfile.ZIP_STORED:
            raise ValueError("EPUB mimetype must be the first uncompressed member")
        container = ET.fromstring(archive.read("META-INF/container.xml"))
        package_path = container.find(".//{*}rootfile").attrib["full-path"]
        package = ET.fromstring(archive.read(package_path))
        language = package.find(".//{http://purl.org/dc/elements/1.1/}language").text
        if language.split("-")[0] != row["language"]:
            raise ValueError(f"incorrect EPUB language: {language}")
        ids = {item.attrib["id"] for item in package.findall(".//{*}manifest/{*}item")}
        spine = package.findall(".//{*}spine/{*}itemref")
        if not spine or any(item.attrib["idref"] not in ids for item in spine):
            raise ValueError("EPUB spine has missing document references")
        return {"language": language, "spine_documents": len(spine), "zip_integrity": "pass"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=ROOT / "dist/publications")
    args = parser.parse_args()
    directory = args.directory.resolve()
    manifest = json.loads((directory / "manifest.json").read_text())
    spec = importlib.util.spec_from_file_location("publications", ROOT / "scripts/render-publications.py")
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    expected = renderer.inventory(ROOT, ("en", "fr"), renderer.COLLECTIONS, ("pdf", "epub"))
    rows = manifest["outputs"]
    errors, checked = [], []
    if (manifest.get("failures") or manifest.get("expected_outputs") != 174
            or Counter(row["output"] for row in rows) != Counter(row["output"] for row in expected)):
        errors.append({"artifact": "manifest", "error": "catalog must contain all 174 unique outputs without build failures"})
    for row in rows:
        try:
            path = directory / row["output"]
            if not path.resolve().is_relative_to(directory):
                raise ValueError("output path escapes the publication directory")
            if sha256(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
                raise ValueError("output hash or size differs from build evidence")
            if renderer.input_hashes(row) != row["inputs"]:
                raise ValueError("source inputs changed after rendering")
            evidence = check_pdf(path, row) if path.suffix == ".pdf" else check_epub(path, row)
            checked.append({"output": row["output"], **evidence})
        except Exception as error:
            errors.append({"artifact": row["output"], "error": str(error)})
    report = {"checked": checked, "errors": errors,
              "limits": "Automatic integrity, freshness, page count and page-boundary checks; not a visual or semantic review."}
    (directory / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Publication validation: {len(checked)}/{len(rows)} outputs passed, {len(errors)} errors")
    for error in errors:
        print(f"- {error['artifact']}: {error['error']}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
