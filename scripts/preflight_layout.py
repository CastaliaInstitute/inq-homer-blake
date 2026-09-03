#!/usr/bin/env python3

"""Verify the requested two-column geometry in rendered proof PDFs."""

from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "output" / "pdf"
TARGETS = [
    PDF_DIR / "inq-homer-iliad-volume-proof.pdf",
    PDF_DIR / "inq-homer-odyssey-volume-proof.pdf",
    PDF_DIR / "inq-homer-odyssey-book-1-proof.pdf",
]


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


if shutil.which("pdftotext") is None:
    fail("pdftotext is required for layout preflight")


def pages(pdf):
    result = subprocess.run(
        ["pdftotext", "-bbox-layout", str(pdf), "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        fail(f"cannot extract layout from {pdf.name}")
    try:
        return ET.fromstring(result.stdout).findall(".//{*}page")
    except ET.ParseError as exc:
        fail(f"invalid bbox XML for {pdf.name}: {exc}")


for pdf in TARGETS:
    if not pdf.is_file():
        fail(f"missing layout target {pdf.relative_to(ROOT)}")
    candidates = []
    for page_number, page in enumerate(pages(pdf), 1):
        width = float(page.attrib.get("width", "0"))
        height = float(page.attrib.get("height", "0"))
        if round(width) != 504 or round(height) != 720:
            fail(f"{pdf.name} page {page_number} is not 504 x 720 points")
        words = []
        for word in page.findall(".//{*}word"):
            text = (word.text or "").strip()
            if not text:
                continue
            words.append((float(word.attrib["xMin"]), float(word.attrib["xMax"]),
                          float(word.attrib["yMin"]), text))
        # Exclude footer furniture and use the inner edges of the two frames;
        # this prevents centered front-matter text from masquerading as columns.
        body = [word for word in words if word[2] < 660]
        left = [word for word in body if word[1] <= 236]
        right = [word for word in body if word[0] >= 268]
        left_lines = {round(word[2]) for word in left}
        right_lines = {round(word[2]) for word in right}
        if len(left_lines) >= 5 and len(right_lines) >= 5:
            candidates.append((page_number, len(left), len(right)))
    if not candidates:
        fail(f"{pdf.name} has no page with text in both columns")
    page_number, left_count, right_count = candidates[0]
    print(f"OK {pdf.relative_to(ROOT)}: two-column text on page {page_number} ({left_count}/{right_count} words)")

print(f"Layout preflight passed: {len(TARGETS)} PDFs contain verified two-column pages.")
