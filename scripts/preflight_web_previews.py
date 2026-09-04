#!/usr/bin/env python3
"""Verify the public Homer samplers are genuine, non-repeating PDF spreads."""

from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess
import sys

from translation_extract import book_translation


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "iliad": {"pages": 9, "words": 4606},
    "odyssey": {"pages": 6, "words": 2629},
}
TOKEN = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?|\d+")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def run(*command: str) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def tokens(text: str) -> list[str]:
    return [token.lower().replace("’", "'") for token in TOKEN.findall(text)]


def is_subsequence(needles: list[str], haystack: list[str]) -> bool:
    cursor = iter(haystack)
    return all(any(candidate == needle for candidate in cursor) for needle in needles)


def inspect(slug: str, expected: dict[str, int]) -> None:
    pdf = ROOT / "output" / "pdf" / f"inq-homer-{slug}-web-preview.pdf"
    if not pdf.is_file():
        fail(f"missing sampler: {pdf.relative_to(ROOT)}")

    info = run("pdfinfo", str(pdf))
    pages = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
    size = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts", info, re.MULTILINE)
    if not pages or int(pages.group(1)) != expected["pages"]:
        fail(f"{slug}: expected {expected['pages']} pages")
    expected_points = (168 * 72 / 25.4, 260 * 72 / 25.4)
    if not size or any(abs(actual - expected_value) > 0.01 for actual, expected_value in zip(map(float, size.groups()), expected_points)):
        fail(f"{slug}: expected exact 168 x 260 mm comic trim")

    image_rows = [
        line.split() for line in run("pdfimages", "-list", str(pdf)).splitlines()
        if re.match(r"^\s*\d+\s+\d+\s+image\s+", line)
    ]
    if len(image_rows) != 2:
        fail(f"{slug}: expected exactly two raster images (cover + one plate), found {len(image_rows)}")
    image_pages = [int(row[0]) for row in image_rows]
    image_sizes = [(int(row[3]), int(row[4])) for row in image_rows]
    if image_pages != [1, 2]:
        fail(f"{slug}: cover and plate must occur only on pages 1 and 2")
    if image_sizes != [(2055, 3142), (2055, 3142)]:
        fail(f"{slug}: cover and plate must both be 2055 x 3142 pixels")

    source_lines = book_translation(ROOT / "text" / slug / "book-01-opening.md")
    source_tokens = tokens("\n".join(source_lines))
    if len(source_tokens) != expected["words"]:
        fail(f"{slug}: source token count changed ({len(source_tokens)} != {expected['words']}); review pagination")
    # Poppler's default reading order follows the PDF's two column frames.
    # ``-layout`` visually interleaves some facing column lines.
    extracted_tokens = tokens(run("pdftotext", str(pdf), "-"))
    if not is_subsequence(source_tokens, extracted_tokens):
        fail(f"{slug}: PDF does not contain the complete current Book I text in order")

    print(
        f"PASS: {slug} — {expected['pages']} pages, canonical trim, "
        f"one cover + one plate, {len(source_tokens)} source tokens"
    )


def main() -> None:
    missing = [tool for tool in ("pdfinfo", "pdfimages", "pdftotext") if shutil.which(tool) is None]
    if missing:
        fail(f"required Poppler tools missing: {', '.join(missing)}")
    for slug, expected in EXPECTED.items():
        inspect(slug, expected)


if __name__ == "__main__":
    main()
