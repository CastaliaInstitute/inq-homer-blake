#!/usr/bin/env python3

"""Check tracked PDF samples and any future release PDFs.

This gate intentionally permits development samples while enforcing the
project's comic-size interior geometry and explicit casewrap cover-proof
geometry. Files named as release interiors/covers
must additionally use embedded fonts and have no encryption.
"""

from pathlib import Path
import shutil
import subprocess
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "output/pdf"
RELEASE_MANIFEST = ROOT / "design/release-manifest.yaml"
TRIM = (477, 738)  # 6.625 x 10.25 inches in points
COVER_PROOF = (1098, 846)  # comic spread with a 0.5 in spine placeholder
BOOKVAULT_PAGE = (174 / 25.4 * 72, 266 / 25.4 * 72)
BOOKVAULT_TRIM = (168 / 25.4 * 72, 260 / 25.4 * 72)


def run(*args):
    return subprocess.run(args, capture_output=True, text=True, check=False)


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


if shutil.which("pdfinfo") is None:
    fail("pdfinfo is required for PDF preflight")
if shutil.which("pdffonts") is None:
    fail("pdffonts is required for PDF preflight")
if shutil.which("pdftotext") is None:
    fail("pdftotext is required for PDF content preflight")

pdfs = sorted(PDF_DIR.glob("*.pdf"))
if not pdfs:
    fail("no PDFs found under output/pdf")

manifest_pages = {}
manifest_file = None
for line in RELEASE_MANIFEST.read_text(encoding="utf-8").splitlines():
    if line.startswith("  - file: "):
        manifest_file = line.split(": ", 1)[1].strip()
    elif manifest_file and line.startswith("    pages: "):
        manifest_pages[manifest_file] = int(line.split(": ", 1)[1].strip())
        manifest_file = None

for pdf in pdfs:
    bookvault_interior = pdf.stem.endswith("-bookvault-interior")
    info = run("pdfinfo", "-box", str(pdf)) if bookvault_interior else run("pdfinfo", str(pdf))
    if info.returncode != 0:
        fail(f"cannot inspect {pdf.relative_to(ROOT)}")
    fields = dict(
        line.split(":", 1) for line in info.stdout.splitlines() if ":" in line
    )
    size = fields.get("Page size", "").strip()
    dimensions = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", size)]
    web_preview = pdf.stem.endswith("-web-preview")
    expected = (
        BOOKVAULT_PAGE if bookvault_interior
        else BOOKVAULT_TRIM if web_preview
        else COVER_PROOF if "cover-design-proof" in pdf.stem
        else TRIM
    )
    size_valid = len(dimensions) >= 2 and (
        all(abs(value - target) < 0.02 for value, target in zip(dimensions[:2], expected))
        if bookvault_interior or web_preview
        else tuple(round(value) for value in dimensions[:2]) == expected
    )
    if not size_valid:
        label = "cover-proof spread" if expected == COVER_PROOF else "exact BookVault trim" if web_preview else "comic trim"
        fail(f"{pdf.name} is not {label}: {fields.get('Page size', 'unknown')}")
    if bookvault_interior:
        trim = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", fields.get("TrimBox", ""))]
        trim_size = (trim[2] - trim[0], trim[3] - trim[1]) if len(trim) == 4 else ()
        if len(trim_size) != 2 or any(abs(value - target) >= 0.02 for value, target in zip(trim_size, BOOKVAULT_TRIM)):
            fail(f"{pdf.name} does not declare the exact 168 x 260 mm TrimBox")
    if fields.get("Encrypted", "").strip().lower() != "no":
        fail(f"{pdf.name} is encrypted")
    manifest_key = str(pdf.relative_to(ROOT))
    if manifest_key in manifest_pages:
        actual_pages = int(fields.get("Pages", "0").strip())
        if actual_pages != manifest_pages[manifest_key]:
            fail(
                f"{pdf.name} page count {actual_pages} disagrees with release manifest "
                f"({manifest_pages[manifest_key]})"
            )

    fonts = run("pdffonts", str(pdf))
    if fonts.returncode != 0:
        fail(f"cannot inspect fonts in {pdf.name}")
    rows = [line.split() for line in fonts.stdout.splitlines()[2:] if line.strip()]
    # Web samplers are editorial distribution previews, not release PDFs; the
    # architecture and cover proofs remain explicitly non-release as well.
    release_pdf = "proof" not in pdf.stem and "web-preview" not in pdf.stem
    if release_pdf and any(len(row) >= 6 and row[3].lower() != "yes" for row in rows):
        fail(f"release PDF {pdf.name} contains a non-embedded font")
    if pdf.stem.endswith("-volume-proof"):
        extracted = run("pdftotext", str(pdf), "-")
        if extracted.returncode != 0:
            fail(f"cannot extract text from {pdf.name}")
        if "WORKING SYNOPSIS" in extracted.stdout.upper():
            fail(f"{pdf.name} contains editorial working-synopsis text")
    print(
        f"OK {pdf.relative_to(ROOT)}: {fields.get('Pages', '?')} pages, "
        f"{fields.get('Page size', '?')}, class={'release' if release_pdf else 'sample'}"
    )

print("PDF preflight passed.")
