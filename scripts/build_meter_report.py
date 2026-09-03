#!/usr/bin/env python3

"""Build a reproducible, heuristic meter-screening report.

This is a triage aid only: syllable estimates cannot establish English stress,
elision, or read-aloud cadence, so the Verse gate remains human-controlled.
"""

from pathlib import Path
import csv
import html
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_volume_proof import book_translation  # noqa: E402

OUT = ROOT / "text" / "meter-report.csv"
SUMMARY = ROOT / "text" / "meter-report.md"


def syllables(word):
    word = re.sub(r"[^a-z']", "", word.lower()).strip("'")
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    groups = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e") and not word.endswith(("le", "ye")) and groups > 1:
        groups -= 1
    if word.endswith("ed") and len(word) > 4 and not word.endswith(("ted", "ded")):
        groups -= 1
    return max(groups, 1)


def score(line):
    words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", html.unescape(line))
    return len(words), sum(syllables(word) for word in words)


rows = []
for volume in ("iliad", "odyssey"):
    for path in sorted((ROOT / "text" / volume).glob("book-*-opening.md")):
        lines = [line for line in book_translation(path) if line.strip()]
        scored = [score(line) for line in lines]
        in_band = [line for line in scored if 8 <= line[1] <= 12]
        outliers = [line for line in scored if line[1] < 8 or line[1] > 12]
        book = int(path.stem.split("-")[1])
        rows.append({
            "volume": volume,
            "book": book,
            "line_count": len(scored),
            "syllable_band_8_12": len(in_band),
            "band_percent": round(100 * len(in_band) / len(scored), 1) if scored else 0,
            "outlier_count": len(outliers),
            "method": "heuristic syllable screen; stress and read-aloud cadence unverified",
            "status": "screening-only",
        })

if len(rows) != 48:
    raise SystemExit(f"expected 48 books, found {len(rows)}")

with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

with SUMMARY.open("w", encoding="utf-8") as handle:
    handle.write("# Meter screening report\n\n")
    handle.write("This report is a reproducible heuristic screen of the working verse. ")
    handle.write("It counts approximate syllables per extracted English line; it does not determine stress, ")
    handle.write("resolve elision, or replace a human read-aloud. No Verse gate may be changed on this report alone.\n\n")
    handle.write("| Volume | Books | Extracted lines | Lines in 8–12 syllable band | Outliers | Status |\n")
    handle.write("|---|---:|---:|---:|---:|---|\n")
    for volume in ("iliad", "odyssey"):
        subset = [row for row in rows if row["volume"] == volume]
        handle.write(f"| {volume.title()} | {len(subset)} | {sum(int(row['line_count']) for row in subset)} | "
                     f"{sum(int(row['syllable_band_8_12']) for row in subset)} | "
                     f"{sum(int(row['outlier_count']) for row in subset)} | screening-only |\n")
    handle.write("\nDetailed per-book values are in [`meter-report.csv`](meter-report.csv). ")
    handle.write("Human review must inspect stress, substitutions, intentional outliers, and read-aloud revisions.\n")

print(f"Wrote {OUT}")
print(f"Wrote {SUMMARY}")
