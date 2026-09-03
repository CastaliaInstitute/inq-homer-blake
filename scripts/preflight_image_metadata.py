#!/usr/bin/env python3
"""Verify plate-manifest image metadata without promoting concept art."""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIN_DPI = 300.0


def fail(message: str) -> None:
    print(f"FAIL image metadata: {message}", file=sys.stderr)
    raise SystemExit(1)


def inspect(path: Path) -> dict[str, str]:
    result = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", "-g", "profile",
         "-g", "dpiWidth", "-g", "dpiHeight", str(path)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        fail(f"cannot inspect {path}")
    values: dict[str, str] = {}
    for line in result.stdout.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip()
    return values


def number(values: dict[str, str], key: str) -> float:
    match = re.search(r"[0-9]+(?:\.[0-9]+)?", values.get(key, ""))
    return float(match.group()) if match else 0.0


manifest = ROOT / "design" / "plate-manifest.csv"
rows = list(csv.DictReader(manifest.open(encoding="utf-8", newline="")))
for row_number, row in enumerate(rows, start=2):
    relative = row["final_file"]
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing {relative} (row {row_number})")
    values = inspect(path)
    width = int(number(values, "pixelWidth"))
    height = int(number(values, "pixelHeight"))
    if (width, height) != (int(row["width_px"]), int(row["height_px"])):
        fail(f"{relative} dimensions differ from manifest (row {row_number})")

    profile = values.get("profile", "")
    declared = row["color_profile"].lower()
    if declared != "unprofiled" and ("nil" in profile.lower() or declared not in profile.lower()):
        fail(f"{relative} declares {row['color_profile']} but embeds {profile or '<missing>'}")

    dpi_width = number(values, "dpiWidth")
    dpi_height = number(values, "dpiHeight")
    if row["curation_status"] == "final":
        if "nil" in profile.lower() or dpi_width < MIN_DPI or dpi_height < MIN_DPI:
            fail(f"final plate {relative} lacks embedded profile or 300 dpi metadata")
    print(f"OK {relative}: {width}x{height}, profile={profile or '<missing>'}, "
          f"dpi={dpi_width:.1f}/{dpi_height:.1f}, status={row['curation_status']}")

print(f"Image metadata preflight passed: {len(rows)} plate records.")
