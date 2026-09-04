#!/usr/bin/env python3
"""Build checksum-bound 300-PPI Iliad print-review derivatives.

These files are technical placement candidates, not native masters or final art.
Human art-direction approval, passage locks, printer color policy, and a physical
proof remain required before publication.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageCms, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
PLATE_MANIFEST = ROOT / "design" / "plate-manifest.csv"
SELECTION_MANIFEST = ROOT / "design" / "iliad-plate-selection.csv"
OUTPUT_DIR = ROOT / "assets" / "print" / "illustrations" / "iliad"
OUTPUT_MANIFEST = OUTPUT_DIR / "manifest.json"
TARGET_SIZE = (2055, 3142)  # 174 x 266 mm including 3 mm bleed at 300 PPI.


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def crop_to_ratio(image: Image.Image) -> tuple[Image.Image, list[int]]:
    target_ratio = TARGET_SIZE[0] / TARGET_SIZE[1]
    source_ratio = image.width / image.height
    if source_ratio > target_ratio:
        width = round(image.height * target_ratio)
        left = (image.width - width) // 2
        box = [left, 0, left + width, image.height]
    else:
        height = round(image.width / target_ratio)
        top = (image.height - height) // 2
        box = [0, top, image.width, top + height]
    return image.crop(tuple(box)), box


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def prepare(source: Path, target: Path) -> dict[str, object]:
    srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    with Image.open(source) as opened:
        source_pixels = [opened.width, opened.height]
        cropped, crop_box = crop_to_ratio(opened.convert("RGB"))
        image = cropped.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        image = image.filter(ImageFilter.UnsharpMask(radius=0.65, percent=65, threshold=2))
        image.save(
            target,
            "JPEG",
            quality=95,
            subsampling=0,
            optimize=True,
            dpi=(300, 300),
            icc_profile=srgb,
        )
    with Image.open(target) as check:
        if check.size != TARGET_SIZE:
            raise ValueError(f"{target}: expected {TARGET_SIZE}, got {check.size}")
        dpi = tuple(round(value) for value in check.info.get("dpi", (0, 0)))
        if dpi != (300, 300):
            raise ValueError(f"{target}: expected 300 PPI, got {dpi}")
        if not check.info.get("icc_profile"):
            raise ValueError(f"{target}: missing embedded sRGB profile")
    return {
        "source": str(source.relative_to(ROOT)),
        "sourcePixels": source_pixels,
        "sourceSha256": sha256(source),
        "cropBoxPixels": crop_box,
        "print": str(target.relative_to(ROOT)),
        "printPixels": list(TARGET_SIZE),
        "printPpi": 300,
        "embeddedProfile": "sRGB",
        "printSha256": sha256(target),
    }


def main() -> None:
    plates = {row["plate_id"]: row for row in load_rows(PLATE_MANIFEST)}
    selections = load_rows(SELECTION_MANIFEST)
    if len(selections) != 24 or {int(row["book"]) for row in selections} != set(range(1, 25)):
        raise ValueError("Iliad selection manifest must contain exactly Books 1 through 24")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    for selection in selections:
        book = int(selection["book"])
        plate = plates.get(selection["plate_id"])
        if plate is None:
            raise ValueError(f"Book {book}: unknown plate ID {selection['plate_id']}")
        if plate["epic"] != "Iliad" or int(plate["book"]) != book:
            raise ValueError(f"Book {book}: selected plate does not belong to this Iliad book")
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
        "work": "The Iliad",
        "artistCredit": "CastaliaInstitute",
        "style": "original ink contour and restrained watercolor informed by the a.Blake house language; not by William Blake",
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
    print(f"Prepared {len(records)} Iliad print-review plates at 2055 x 3142 / 300 PPI")
    print(OUTPUT_MANIFEST)


if __name__ == "__main__":
    main()
