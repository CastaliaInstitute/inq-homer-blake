#!/usr/bin/env python3

"""Build a deterministic production handoff report from current artifacts."""

from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from translation_extract import book_translation

OUT = ROOT / "design" / "preflight-report.md"
PDFS = [
    ("Iliad interior proof", ROOT / "output/pdf/inq-homer-iliad-volume-proof.pdf"),
    ("Odyssey interior proof", ROOT / "output/pdf/inq-homer-odyssey-volume-proof.pdf"),
    ("Iliad BookVault prepress interior", ROOT / "output/pdf/inq-homer-iliad-bookvault-interior.pdf"),
    ("Odyssey BookVault prepress interior", ROOT / "output/pdf/inq-homer-odyssey-bookvault-interior.pdf"),
    ("Iliad cover study", ROOT / "output/pdf/inq-homer-iliad-cover-design-proof.pdf"),
    ("Odyssey cover study", ROOT / "output/pdf/inq-homer-odyssey-cover-design-proof.pdf"),
]


def pdf_info(path):
    result = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=True)
    values = {}
    for line in result.stdout.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip()
    return values


with (ROOT / "design/plate-manifest.csv").open(newline="", encoding="utf-8") as stream:
    plates = list(csv.DictReader(stream))
with (ROOT / "design/architecture-page-map.csv").open(newline="", encoding="utf-8") as stream:
    page_map = list(csv.DictReader(stream))
with (ROOT / "text/translation-status.csv").open(newline="", encoding="utf-8") as stream:
    statuses = list(csv.DictReader(stream))
iliad_print_manifest = ROOT / "assets/print/illustrations/iliad/manifest.json"
if not iliad_print_manifest.is_file():
    raise SystemExit(f"missing Iliad print-art manifest: {iliad_print_manifest}")
iliad_print = json.loads(iliad_print_manifest.read_text(encoding="utf-8"))
odyssey_print_manifest = ROOT / "assets/print/illustrations/odyssey/manifest.json"
if not odyssey_print_manifest.is_file():
    raise SystemExit(f"missing Odyssey print-art manifest: {odyssey_print_manifest}")
odyssey_print = json.loads(odyssey_print_manifest.read_text(encoding="utf-8"))
bookvault_manifest = json.loads(
    (ROOT / "output/pdf/inq-homer-bookvault-interiors.manifest.json").read_text(encoding="utf-8")
)
stale_bookvault_sources = []
for volume, record in bookvault_manifest["volumes"].items():
    for book in record["books"]:
        source = ROOT / book["source"]
        current = hashlib.sha256(source.read_bytes()).hexdigest()
        if current != book["sourceSha256"]:
            stale_bookvault_sources.append(f"{volume} {book['book']}")

density_holds = 0
for status in statuses:
    path = ROOT / status["translation_file"]
    text = path.read_text(encoding="utf-8")
    ranges = re.findall(r"\*\*Source passage:\*\* Book \d+, lines (\d+)[–-](\d+)", text)
    if not ranges:
        raise SystemExit(f"cannot measure translation density: {path}")
    source_lines = max(int(end) for _, end in ranges) - min(int(start) for start, _ in ranges) + 1
    words = len(re.findall(r"\b[\w’'-]+\b", " ".join(book_translation(path))))
    if words / source_lines < 5.0:
        density_holds += 1

lines = [
    "# Current production preflight report",
    "",
    "This report is generated from the tracked proofs and manifests. It is a",
    "handoff snapshot, not a release certificate; all human and printer gates",
    "must still be closed in `design/release-readiness.md`.",
    "",
    "## Edition target",
    "",
    "- Trim: 6.625 × 10.25 inches (comic size), with BookVault's provisional 168 × 260 mm candidate route documented separately",
    "- Interior: two columns, hardcover, 80# White Coated, Premium Color target",
    "- Cover studies: one-page integrated casewrap spreads; printer-specific template required after page-count lock",
    "",
    "## Proof inventory",
    "",
    "| Artifact | Pages | Page size | Encryption |",
    "|---|---:|---|---|",
]
for label, path in PDFS:
    if not path.is_file():
        raise SystemExit(f"missing proof: {path}")
    info = pdf_info(path)
    lines.append(f"| {label} | {info.get('Pages', '?')} | {info.get('Page size', '?')} | {info.get('Encrypted', '?')} |")

lines += [
    "",
    "## Coverage and provenance",
    "",
    f"- Translation ledger: {len(statuses)} books; all remain under review.",
    f"- Reader-facing density screen: {density_holds} provisional holds; see `design/translation-density-report.md`.",
    f"- Architecture page map: {len(page_map)} traced pages.",
    f"- Plate manifest: {len(plates)} records; all concept/source-review, none final.",
    f"- Iliad print-review art: {iliad_print['plateCount']} checksum-bound 2055 × 3142 / 300-PPI sRGB derivatives; human approval pending.",
    f"- Odyssey print-review art: {odyssey_print['plateCount']} checksum-bound 2055 × 3142 / 300-PPI sRGB derivatives; human approval pending.",
    (
        f"- BookVault source lock: {len(stale_bookvault_sources)} stale manuscript reference(s); "
        + ("rebuild required before candidate validation." if stale_bookvault_sources else "candidate hashes match current manuscript sources.")
    ),
    "- Asset checksums: `design/asset-checksums.csv`, rebuilt in CI.",
    "- Font evidence: `design/font-lock.md`; Cormorant Garamond OFL 1.1 files tracked.",
    "",
    "## Release blockers",
    "",
    "1. Named independent Greek-fidelity review for all 48 books.",
    "2. Separate literary, meter, and notes/glossary approvals.",
    "3. Art-direction selection, passage/caption locks, and rights confirmation.",
    "4. Final printer profile, cover templates, spine widths, and binding lock.",
    "5. Rebuild the stale BookVault candidates after text lock, then run PDF, trim, profile, overprint, font, and source-hash checks.",
    "6. Physical or printer proof inspection and dated correction record.",
]

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {OUT}")
