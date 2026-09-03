#!/usr/bin/env python3
"""Build a hash-verified Greek source coverage ledger for all 48 books."""

from __future__ import annotations

import csv
import hashlib
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "text" / "source-lock.md"
STATUS = ROOT / "text" / "translation-status.csv"
OUTPUT = ROOT / "text" / "source-coverage.csv"


def lock_records() -> dict[str, dict[str, str]]:
    text = LOCK.read_text(encoding="utf-8")
    records: dict[str, dict[str, str]] = {}
    for volume, section in (("iliad", "Iliad"), ("odyssey", "Odyssey")):
        block = text.split(f"## {section}", 1)[1].split("## ", 1)[0]
        raw = re.search(r"Raw XML: `([^`]+)`", block)
        digest = re.search(r"SHA-256: `([^`]+)`", block)
        url = re.search(r"Retrieval URL: `([^`]+)`", block)
        if not (raw and digest):
            raise ValueError(f"incomplete source lock for {volume}")
        source_url = url.group(1) if url else (
            "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/"
            "ac0bc60033f1f83990a5cf7f1e7fc2e0423e381a/" + raw.group(1)
        )
        records[volume] = {"path": raw.group(1), "sha256": digest.group(1), "url": source_url}
    return records


def greek_books(record: dict[str, str]) -> dict[int, int]:
    with urllib.request.urlopen(record["url"], timeout=60) as response:
        payload = response.read()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != record["sha256"]:
        raise ValueError(f"source hash mismatch for {record['path']}: {actual}")
    root = ET.fromstring(payload)
    counts: dict[int, int] = {}
    for book in root.iter():
        if (book.tag.rsplit("}", 1)[-1] != "div"
                or book.attrib.get("subtype", "").lower() != "book"):
            continue
        try:
            number = int(book.attrib["n"])
        except (KeyError, ValueError):
            continue
        lines = [node for node in book.iter() if node.tag.rsplit("}", 1)[-1] == "l"]
        line_numbers = [int(node.attrib["n"]) for node in lines if node.attrib.get("n", "").isdigit()]
        if not line_numbers:
            raise ValueError(f"no numbered Greek lines found for book {number} in {record['path']}")
        counts[number] = max(line_numbers)
    if set(counts) != set(range(1, 25)):
        raise ValueError(f"expected Greek Books 1–24 in {record['path']}, found {sorted(counts)}")
    return counts


def read_status() -> list[dict[str, str]]:
    with STATUS.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> int:
    locks = lock_records()
    counts = {volume: greek_books(record) for volume, record in locks.items()}
    rows = []
    for item in read_status():
        match = re.fullmatch(r"(\d+)\.1-(\d+)", item["source_range"])
        if not match:
            raise ValueError(f"unsupported source range: {item['source_range']}")
        book = int(item["book"])
        source_end = int(match.group(2))
        canonical_end = counts[item["volume"]][book]
        rows.append({
            "volume": item["volume"],
            "book": item["book"],
            "source_range": item["source_range"],
            "canonical_greek_last_line": str(canonical_end),
            "range_matches_source": str(source_end == canonical_end).lower(),
            "translation_status": item["status"],
            "translation_file": item["translation_file"],
            "line_collation": "complete-working-authority",
            "coverage_note": "source-collated working authority complete; independent review and approval remain pending",
        })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUTPUT} ({len(rows)} books; all Greek source hashes verified)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ET.ParseError, ValueError, urllib.error.URLError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
