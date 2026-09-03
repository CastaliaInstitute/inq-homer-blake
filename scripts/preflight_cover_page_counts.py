#!/usr/bin/env python3

"""Verify cover-study page labels agree with the release manifest."""

from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "design" / "release-manifest.yaml"

manifest_text = MANIFEST.read_text(encoding="utf-8")
expected = {}
for volume in ("iliad", "odyssey"):
    pattern = (
        rf"- file: output/pdf/inq-homer-{volume}-volume-proof\.pdf"
        rf"(?P<body>(?:\n    .*?)*)(?:\n  - file:|\Z)"
    )
    match = re.search(pattern, manifest_text, re.DOTALL)
    if not match:
        raise SystemExit(f"FAIL: no manifest page count for {volume} volume proof")
    pages_match = re.search(r"\n    pages: (\d+)", match.group("body"))
    if not pages_match:
        raise SystemExit(f"FAIL: no page count in {volume} volume-proof block")
    expected[volume] = int(pages_match.group(1))

for volume, pages in expected.items():
    pdf = ROOT / f"output/pdf/inq-homer-{volume}-cover-design-proof.pdf"
    text = subprocess.run(
        ["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True
    ).stdout
    match = re.search(r"Current architecture proof: (\d+) pages", text)
    if not match:
        raise SystemExit(f"FAIL: {pdf} has no architecture page-count label")
    actual = int(match.group(1))
    if actual != pages:
        raise SystemExit(
            f"FAIL: {pdf.name} says {actual} pages; manifest says {pages}"
        )
    print(f"OK {pdf}: cover label and manifest both say {pages} pages")

print("Cover-study page-count preflight passed.")
