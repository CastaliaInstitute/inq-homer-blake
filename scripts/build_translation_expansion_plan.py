#!/usr/bin/env python3

"""Build the actionable queue for reader-facing translation expansion."""

from pathlib import Path
import csv
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from translation_extract import book_translation

THRESHOLD = 5.0
rows = []

with (ROOT / "text/translation-status.csv").open(newline="", encoding="utf-8") as stream:
    ledger = list(csv.DictReader(stream))

for record in ledger:
    if record["status"] == "outline":
        continue
    path = ROOT / record["translation_file"]
    text = path.read_text(encoding="utf-8")
    ranges = re.findall(r"\*\*Source passage:\*\* Book \d+, lines (\d+)[–-](\d+)", text)
    if not ranges:
        raise SystemExit(f"cannot measure {path}")
    source_lines = max(int(end) for _, end in ranges) - min(int(start) for start, _ in ranges) + 1
    words = len(re.findall(r"\b[\w’'-]+\b", " ".join(book_translation(path))))
    target = int(source_lines * THRESHOLD + 0.9999)
    density = words / source_lines
    if density < THRESHOLD:
        rows.append({
            "volume": record["volume"], "book": int(record["book"]),
            "file": record["translation_file"], "source_lines": source_lines,
            "words": words, "minimum_screen_target": target,
            "additional_words": target - words, "density": density,
        })

rows.sort(key=lambda row: (row["volume"], row["book"]))
out = ROOT / "design/translation-expansion-plan.md"
with out.open("w", encoding="utf-8") as handle:
    handle.write("# Translation expansion plan\n\n")
    handle.write("This queue is generated from the reader-facing Translation sections and their declared source ranges. It is a triage floor, not a word-count prescription: expansion must preserve the full narrative, then pass independent Greek-fidelity, literary, meter, notes, and read-aloud review. The screen floor is 5.0 English words per source line.\n\n")
    handle.write("Work in source order within each volume. For every book, compare the expanded English line by line against the pinned Greek, record omissions/additions and adopted readings in the book packet, then rerun the density and meter screens.\n\n")
    handle.write("| Priority | Volume | Book | Source lines | Current words | Screen-floor words | Additional words to floor | Current density | Working file |\n")
    handle.write("|---:|---|---:|---:|---:|---:|---:|---:|---|\n")
    for priority, row in enumerate(rows, 1):
        handle.write(f"| {priority} | {row['volume']} | {row['book']} | {row['source_lines']} | {row['words']} | {row['minimum_screen_target']} | {row['additional_words']} | {row['density']:.2f} | `{row['file']}` |\n")
    handle.write(f"\n**Open queue:** {len(rows)} books. A book leaves this queue only after expansion and documented editorial review; a density screen-pass does not itself approve a translation.\n")

print(f"Wrote {out} ({len(rows)} expansion holds)")
