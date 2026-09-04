#!/usr/bin/env python3
"""Validate Homer editorial EPUB structure and fail-closed release metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/epub"
OPF = "http://www.idpf.org/2007/opf"
DC = "http://purl.org/dc/elements/1.1/"


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate(volume: str, epubcheck_jar: Path | None, require_epubcheck: bool) -> dict:
    epub = OUTPUT / f"inq-homer-{volume}-editorial-proof.epub"
    manifest_path = OUTPUT / f"inq-homer-{volume}-editorial-proof.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    data = epub.read_bytes()
    require(sha256(data) == manifest["epubSha256"], "EPUB checksum differs from build manifest")
    require(manifest["releaseClass"] == "private_editorial_proof", "release class must remain private editorial proof")
    require(manifest["saleApproved"] is False, "editorial EPUB must not be approved for sale")
    require(manifest["publicDistributionApproved"] is False, "editorial EPUB must not be approved for public distribution")
    require(manifest["books"] == 24, "EPUB must contain 24 books")
    require(manifest["illustrationPlates"] == 0, "unapproved plate art must not be embedded")
    require("Longfellow-inspired" in manifest["translator"], "translation credit must describe inspiration without false attribution")
    require(manifest["illustrator"] is None, "illustration-free proof must not carry an illustrator credit")
    require(manifest["illustrationCredit"].startswith("No illustrations included"), "illustration-free proof must state that no illustrations are included")
    require(set(manifest["openEditorialGates"]) == {"greek_fidelity", "literary", "meter", "notes_glossary", "art_direction", "cover_art", "production", "epubcheck", "physical_proof"}, "all editorial and production gates must remain explicit")
    require(manifest["coverStatus"] == "text_only_unapproved_misattributed_cover_art_omitted", "unsafe cover art must remain omitted")
    source = ROOT / manifest["source"]
    require(sha256(source.read_bytes()) == manifest["sourceSha256"], "source export checksum differs")

    with zipfile.ZipFile(epub) as archive:
        names = archive.namelist()
        require(names[0] == "mimetype", "mimetype must be first")
        require(archive.getinfo("mimetype").compress_type == zipfile.ZIP_STORED, "mimetype must be uncompressed")
        require(archive.read("mimetype") == b"application/epub+zip", "invalid mimetype")
        package = ET.fromstring(archive.read("OEBPS/package.opf"))
        rights = package.findtext(f".//{{{DC}}}rights")
        require(rights == "Private editorial proof. Not approved for sale or public distribution.", "package must carry the fail-closed rights notice")
        require(package.findtext(f".//{{{DC}}}creator") == "Homer", "creator must be Homer")
        require(package.findtext(f".//{{{DC}}}source") == manifest["sourceEdition"], "package source edition must match the manifest")
        contributor = package.find(f".//{{{DC}}}contributor[@id='translator']")
        require(contributor is not None and contributor.text == "Castalia Institute", "translator must be identified as Castalia Institute")
        metadata = package.find(f".//{{{OPF}}}metadata")
        metas = {(item.attrib.get("property"), (item.text or "").strip()) for item in metadata.findall(f"{{{OPF}}}meta")}
        require(("role", "trl") in metas, "translator MARC role is missing")
        require(("schema:accessMode", "textual") in metas, "textual accessibility mode is missing")
        require(("schema:accessibilityFeature", "structuralNavigation") in metas, "structural-navigation metadata is missing")
        require(("schema:accessibilityFeature", "tableOfContents") in metas, "table-of-contents metadata is missing")
        require(("schema:accessibilityHazard", "none") in metas, "accessibility hazard metadata is missing")
        items = package.findall(f".//{{{OPF}}}manifest/{{{OPF}}}item")
        for item in items:
            require("OEBPS/" + item.attrib["href"] in names, f"missing package item: {item.attrib['href']}")
        for number in range(1, 25):
            require(f"OEBPS/text/book-{number:02}.xhtml" in names, f"Book {number} is missing")
        for name in names:
            if name.endswith((".xhtml", ".opf", ".xml")):
                root = ET.fromstring(archive.read(name))
                if name.endswith(".xhtml"):
                    require(root.attrib.get("lang") == "en", f"{name} must declare lang=en")
                    require(root.attrib.get("{http://www.w3.org/XML/1998/namespace}lang") == "en", f"{name} must declare xml:lang=en")
        require(not any("plate" in name.lower() for name in names), "plate assets must remain absent until approved")
        require(not any(name.startswith("OEBPS/images/") for name in names), "unapproved cover or plate images must remain absent")

    check = "not available"
    if epubcheck_jar:
        result = subprocess.run(["java", "-jar", str(epubcheck_jar), str(epub)], text=True, capture_output=True)
        if result.returncode:
            sys.stderr.write(result.stdout + result.stderr)
            raise ValueError("EPUBCheck failed")
        check = "EPUBCheck clean"
    elif executable := shutil.which("epubcheck"):
        result = subprocess.run([executable, str(epub)], text=True, capture_output=True)
        if result.returncode:
            sys.stderr.write(result.stdout + result.stderr)
            raise ValueError("EPUBCheck failed")
        check = "EPUBCheck clean"
    elif require_epubcheck:
        raise ValueError("EPUBCheck is required but is not installed")
    return {"valid": True, "volume": volume, "epub": str(epub), "sha256": manifest["epubSha256"], "books": 24, "saleApproved": False, "epubcheck": check}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--volume", choices=["iliad", "odyssey", "all"], default="all")
    parser.add_argument("--epubcheck-jar", type=Path)
    parser.add_argument("--require-epubcheck", action="store_true")
    args = parser.parse_args()
    selected = ("iliad", "odyssey") if args.volume == "all" else (args.volume,)
    try:
        print(json.dumps([validate(volume, args.epubcheck_jar, args.require_epubcheck) for volume in selected], indent=2))
    except (OSError, KeyError, ValueError, zipfile.BadZipFile, ET.ParseError) as error:
        print(json.dumps({"valid": False, "error": str(error)}, indent=2))
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
