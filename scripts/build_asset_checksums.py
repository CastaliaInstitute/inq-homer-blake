#!/usr/bin/env python3

"""Build a deterministic checksum ledger for every plate-manifest asset."""

from pathlib import Path
import csv
import hashlib

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "design" / "plate-manifest.csv"
OUT = ROOT / "design" / "asset-checksums.csv"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


rows = []
with MANIFEST.open(newline="", encoding="utf-8") as stream:
    for record in csv.DictReader(stream):
        path = ROOT / record["final_file"]
        if not path.is_file():
            raise SystemExit(f"missing plate asset: {record['final_file']}")
        rows.append({
            "plate_id": record["plate_id"],
            "final_file": record["final_file"],
            "sha256": sha256(path),
            "width_px": record["width_px"],
            "height_px": record["height_px"],
            "color_profile": record["color_profile"],
            "curation_status": record["curation_status"],
        })

fields = ["plate_id", "final_file", "sha256", "width_px", "height_px",
          "color_profile", "curation_status"]
with OUT.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {OUT} ({len(rows)} assets)")
