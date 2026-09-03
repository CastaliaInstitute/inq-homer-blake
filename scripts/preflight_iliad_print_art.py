#!/usr/bin/env python3
"""Verify the selected Iliad print-review derivatives and their lineage."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "design" / "iliad-plate-selection.csv"
PLATES = ROOT / "design" / "plate-manifest.csv"
MANIFEST = ROOT / "assets" / "print" / "illustrations" / "iliad" / "manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def image_values(path: Path) -> tuple[tuple[int, int], tuple[float, float], bool]:
    with Image.open(path) as image:
        size = image.size
        dpi = image.info.get("dpi", (0.0, 0.0))
        profile = bool(image.info.get("icc_profile"))
    return size, (float(dpi[0]), float(dpi[1])), profile


def main() -> None:
    selections = csv_rows(SELECTION)
    if len(selections) != 24 or {int(row["book"]) for row in selections} != set(range(1, 25)):
        raise SystemExit("FAIL: selection must contain exactly Iliad Books 1 through 24")
    if any(row["approval_status"] != "pending" for row in selections):
        raise SystemExit("FAIL: print-review selections must not imply human approval")

    plate_rows = {row["plate_id"]: row for row in csv_rows(PLATES)}
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("plateCount") != 24 or len(data.get("plates", [])) != 24:
        raise SystemExit("FAIL: print manifest must contain 24 plates")
    if data.get("historicalScansIncluded") is not False or data.get("nativeMasterClaim") is not False:
        raise SystemExit("FAIL: print manifest must exclude historical scans and native-master claims")
    if data.get("trimMm") != [168, 260] or data.get("documentMm") != [174, 266] or data.get("bleedMm") != 3:
        raise SystemExit("FAIL: print manifest geometry is not canonical iNQ comic size")

    selected = {int(row["book"]): row for row in selections}
    for record in data["plates"]:
        book = int(record["book"])
        selection = selected.get(book)
        if not selection or record["plateId"] != selection["plate_id"]:
            raise SystemExit(f"FAIL: Book {book} print lineage differs from selection")
        plate = plate_rows.get(record["plateId"])
        if not plate or plate["source_type"] != "generated" or plate["epic"] != "Iliad":
            raise SystemExit(f"FAIL: Book {book} must use an original generated Iliad candidate")

        source = ROOT / record["source"]
        target = ROOT / record["print"]
        if not source.is_file() or not target.is_file():
            raise SystemExit(f"FAIL: Book {book} source or print derivative is missing")
        if sha256(source) != record["sourceSha256"] or sha256(target) != record["printSha256"]:
            raise SystemExit(f"FAIL: Book {book} source or print checksum changed")
        size, dpi, has_profile = image_values(target)
        if list(size) != [2055, 3142]:
            raise SystemExit(f"FAIL: Book {book} has invalid print dimensions")
        if round(dpi[0]) != 300 or round(dpi[1]) != 300:
            raise SystemExit(f"FAIL: Book {book} is not tagged 300 PPI")
        if not has_profile:
            raise SystemExit(f"FAIL: Book {book} has no embedded sRGB profile")

    print("PASS Iliad print art: 24 checksum-bound 2055 × 3142 / 300-PPI sRGB review derivatives")


if __name__ == "__main__":
    main()
