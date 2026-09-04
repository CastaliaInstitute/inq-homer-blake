#!/usr/bin/env python3
"""Build checksum-bound 300-PPI Odyssey print-review derivatives."""

from __future__ import annotations

import json

from prepare_iliad_print_art import ROOT, load_rows, prepare


PLATE_MANIFEST = ROOT / "design" / "plate-manifest.csv"
SELECTION_MANIFEST = ROOT / "design" / "odyssey-plate-selection.csv"
OUTPUT_DIR = ROOT / "assets" / "print" / "illustrations" / "odyssey"
OUTPUT_MANIFEST = OUTPUT_DIR / "manifest.json"


def main() -> None:
    plates = {row["plate_id"]: row for row in load_rows(PLATE_MANIFEST)}
    selections = load_rows(SELECTION_MANIFEST)
    if len(selections) != 24 or {int(row["book"]) for row in selections} != set(range(1, 25)):
        raise ValueError("Odyssey selection manifest must contain exactly Books 1 through 24")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    for selection in selections:
        book = int(selection["book"])
        plate = plates.get(selection["plate_id"])
        if plate is None:
            raise ValueError(f"Book {book}: unknown plate ID {selection['plate_id']}")
        if plate["epic"] != "Odyssey" or int(plate["book"]) != book:
            raise ValueError(f"Book {book}: selected plate does not belong to this Odyssey book")
        if plate["source_type"] != "generated" or plate["curation_status"] == "final":
            raise ValueError(f"Book {book}: expected a non-final generated candidate")
        if selection["approval_status"] != "pending":
            raise ValueError(f"Book {book}: this script only handles pending review selections")

        source = ROOT / plate["final_file"]
        if not source.is_file():
            raise FileNotFoundError(f"Book {book}: missing source plate {source}")
        target = OUTPUT_DIR / f"book-{book:02d}-full-bleed.jpg"
        records.append(
            {
                "book": book,
                "plateId": selection["plate_id"],
                "subject": plate["caption"],
                "passage": plate["passage"],
                "selectionStatus": selection["selection_status"],
                "approvalStatus": selection["approval_status"],
                **prepare(source, target),
            }
        )

    manifest = {
        "schemaVersion": 1,
        "work": "The Odyssey",
        "artistCredit": "CastaliaInstitute",
        "style": "original ink contour and restrained watercolor informed by the repository's Blake-informed house language; not by William Blake",
        "historicalScansIncluded": False,
        "reviewStatus": "print-review derivatives; human art-direction and physical proof pending",
        "nativeMasterClaim": False,
        "trimMm": [168, 260],
        "bleedMm": 3,
        "documentMm": [174, 266],
        "plateCount": len(records),
        "plates": records,
    }
    OUTPUT_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Prepared 24 Odyssey print-review plates at 2055 x 3142 / 300 PPI")
    print(OUTPUT_MANIFEST)


if __name__ == "__main__":
    main()
