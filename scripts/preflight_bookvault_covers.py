#!/usr/bin/env python3
"""Fail closed on tracked BookVault cover bundles that are not release-safe.

Workspace-only template experiments are intentionally ignored. If a cover
bundle is committed, its adjacent manifest must keep it non-production until
the printer template, credits, rights, and physical proof are approved.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "output/bookvault"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [ROOT / line for line in result.stdout.splitlines() if line]


def main() -> None:
    paths = tracked_paths()
    manifests = [path for path in paths if path.suffix == ".json" and path.name.endswith(".manifest.json")]
    if not manifests:
        print("BookVault cover safety preflight passed: no tracked cover bundles")
        return

    errors: list[str] = []
    for manifest_path in manifests:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if data.get("productionEligible") is not False:
            errors.append(f"{manifest_path.relative_to(ROOT)} must remain productionEligible=false")
        pdf_name = data.get("output")
        if not pdf_name:
            errors.append(f"{manifest_path.relative_to(ROOT)} lacks output path")
            continue
        pdf_path = ROOT / Path(pdf_name).relative_to(ROOT) if str(pdf_name).startswith(str(ROOT)) else ROOT / Path(pdf_name)
        if pdf_path.is_file():
            text = subprocess.run(["pdftotext", str(pdf_path), "-"], check=True, capture_output=True, text=True).stdout
            for unsafe in ("A.Longfellow", "A.Blake", "a.Longfellow", "a.Blake"):
                if unsafe in text:
                    errors.append(f"{pdf_path.relative_to(ROOT)} contains unsafe credit {unsafe!r}")
    if errors:
        raise SystemExit("BookVault cover safety preflight failed:\n- " + "\n- ".join(errors))
    print(f"BookVault cover safety preflight passed: {len(manifests)} tracked bundles remain fail-closed")


if __name__ == "__main__":
    main()
