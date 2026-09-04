#!/usr/bin/env python3
"""Verify both Homer volumes' print-review art and source lineage."""

from __future__ import annotations

import json

from preflight_iliad_print_art import ROOT, csv_rows, image_values, sha256


def validate(work: str) -> None:
    slug = work.lower()
    selections = csv_rows(ROOT / "design" / f"{slug}-plate-selection.csv")
    if len(selections) != 24 or {int(row["book"]) for row in selections} != set(range(1, 25)):
        raise SystemExit(f"FAIL: {work} selection must contain exactly Books 1 through 24")
    if any(row["approval_status"] != "pending" for row in selections):
        raise SystemExit(f"FAIL: {work} print-review selections must not imply human approval")

    plate_rows = {row["plate_id"]: row for row in csv_rows(ROOT / "design" / "plate-manifest.csv")}
    manifest = ROOT / "assets" / "print" / "illustrations" / slug / "manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("work") != f"The {work}" or data.get("plateCount") != 24 or len(data.get("plates", [])) != 24:
        raise SystemExit(f"FAIL: {work} print manifest identity or count is invalid")
    if data.get("historicalScansIncluded") is not False or data.get("nativeMasterClaim") is not False:
        raise SystemExit(f"FAIL: {work} manifest must exclude historical scans and native-master claims")
    if data.get("artistCredit") != "CastaliaInstitute" or "not by William Blake" not in data.get("style", ""):
        raise SystemExit(f"FAIL: {work} manifest must credit the documented creator and disclaim William Blake authorship")
    if data.get("trimMm") != [168, 260] or data.get("documentMm") != [174, 266] or data.get("bleedMm") != 3:
        raise SystemExit(f"FAIL: {work} print geometry is not canonical iNQ comic size")

    selected = {int(row["book"]): row for row in selections}
    for record in data["plates"]:
        book = int(record["book"])
        selection = selected.get(book)
        if not selection or record["plateId"] != selection["plate_id"]:
            raise SystemExit(f"FAIL: {work} Book {book} lineage differs from selection")
        plate = plate_rows.get(record["plateId"])
        if not plate or plate["source_type"] != "generated" or plate["epic"] != work:
            raise SystemExit(f"FAIL: {work} Book {book} must use an original generated candidate")
        source, target = ROOT / record["source"], ROOT / record["print"]
        if not source.is_file() or not target.is_file():
            raise SystemExit(f"FAIL: {work} Book {book} source or derivative is missing")
        if sha256(source) != record["sourceSha256"] or sha256(target) != record["printSha256"]:
            raise SystemExit(f"FAIL: {work} Book {book} checksum changed")
        size, dpi, has_profile = image_values(target)
        if list(size) != [2055, 3142] or round(dpi[0]) != 300 or round(dpi[1]) != 300 or not has_profile:
            raise SystemExit(f"FAIL: {work} Book {book} dimensions, PPI, or profile is invalid")

    print(f"PASS {work} print art: 24 checksum-bound 2055 × 3142 / 300-PPI sRGB review derivatives")


def main() -> None:
    validate("Iliad")
    validate("Odyssey")


if __name__ == "__main__":
    main()
