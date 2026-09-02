#!/usr/bin/env python3

"""Check tracked PDF samples and any future release PDFs.

This gate intentionally permits development samples while enforcing the
project's 7 x 10 inch page geometry. Files named as release interiors/covers
must additionally use embedded fonts and have no encryption.
"""

from pathlib import Path
import shutil
import subprocess
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "output/pdf"
TRIM = (504, 720)  # 7 x 10 inches in points


def run(*args):
    return subprocess.run(args, capture_output=True, text=True, check=False)


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


if shutil.which("pdfinfo") is None:
    fail("pdfinfo is required for PDF preflight")
if shutil.which("pdffonts") is None:
    fail("pdffonts is required for PDF preflight")

pdfs = sorted(PDF_DIR.glob("*.pdf"))
if not pdfs:
    fail("no PDFs found under output/pdf")

for pdf in pdfs:
    info = run("pdfinfo", str(pdf))
    if info.returncode != 0:
        fail(f"cannot inspect {pdf.relative_to(ROOT)}")
    fields = dict(
        line.split(":", 1) for line in info.stdout.splitlines() if ":" in line
    )
    size = fields.get("Page size", "").strip()
    dimensions = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", size)]
    if len(dimensions) < 2 or tuple(round(value) for value in dimensions[:2]) != TRIM:
        fail(f"{pdf.name} is not 7 x 10 in: {fields.get('Page size', 'unknown')}")
    if fields.get("Encrypted", "").strip().lower() != "no":
        fail(f"{pdf.name} is encrypted")

    fonts = run("pdffonts", str(pdf))
    if fonts.returncode != 0:
        fail(f"cannot inspect fonts in {pdf.name}")
    rows = [line.split() for line in fonts.stdout.splitlines()[2:] if line.strip()]
    release_pdf = "proof" not in pdf.stem
    if release_pdf and any(len(row) >= 6 and row[3].lower() != "yes" for row in rows):
        fail(f"release PDF {pdf.name} contains a non-embedded font")
    print(
        f"OK {pdf.relative_to(ROOT)}: {fields.get('Pages', '?')} pages, "
        f"{fields.get('Page size', '?')}, class={'release' if release_pdf else 'sample'}"
    )

print("PDF preflight passed.")
