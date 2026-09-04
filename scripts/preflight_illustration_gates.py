#!/usr/bin/env python3
"""Fail-closed checks for the five independent illustration release gates."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "design" / "plate-selection-audit.csv"
REQUIRED = (
    "art_direction_gate",
    "caption_range_gate",
    "rights_credit_gate",
    "native_master_gate",
    "physical_proof_gate",
)
ALLOWED = {"pending", "pass", "hold", "revise"}


def main() -> None:
    with AUDIT.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        rows = list(reader)

    missing = [field for field in REQUIRED if field not in fields]
    if missing:
        raise SystemExit(f"illustration audit missing gate fields: {', '.join(missing)}")
    if len(rows) != 48:
        raise SystemExit(f"illustration audit must contain 48 rows, found {len(rows)}")

    keys = {(row["volume"], row["book"]) for row in rows}
    if len(keys) != 48:
        raise SystemExit("illustration audit contains duplicate volume/book slots")

    errors: list[str] = []
    for row in rows:
        label = f"{row['volume']} Book {row['book']}"
        for field in REQUIRED:
            value = row[field]
            if value not in ALLOWED:
                errors.append(f"{label}: {field} has invalid value {value!r}")
            if row["selection_status"] == "provisional-print-review" and value != "pending":
                errors.append(f"{label}: provisional selection has non-pending {field}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Illustration gate preflight passed: {len(rows)} slots × {len(REQUIRED)} independent gates; provisional gates remain pending.")


if __name__ == "__main__":
    main()
