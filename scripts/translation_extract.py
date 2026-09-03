#!/usr/bin/env python3

"""Extract the authoritative translated lines without PDF-builder dependencies."""

from pathlib import Path
import re
from xml.sax.saxutils import escape


def book_translation(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    if "compact translation" in content.lower():
        authorities = []
        for candidate in sorted(path.parent.glob(f"{path.stem.replace('-opening', '')}-collation-*.md")):
            authority = candidate.read_text(encoding="utf-8")
            if "## Revised translation pass" in authority:
                range_match = re.search(r"collation-(\d+)-(\d+)\.md$", candidate.name)
                if range_match:
                    authorities.append((int(range_match.group(1)), int(range_match.group(2)), authority))
        source_range = re.search(r"Source passage:.*?Book \d+, lines\s+1\D+(\d+)", content, re.S)
        authorities.sort(key=lambda item: item[0])
        covers_book = bool(source_range and authorities and authorities[0][0] == 1)
        if covers_book:
            expected_end = int(source_range.group(1))
            cursor = 1
            for start, end, _ in authorities:
                if start != cursor:
                    covers_book = False
                    break
                cursor = end + 1
            covers_book = covers_book and cursor - 1 == expected_end
        if covers_book:
            bodies = []
            for _, _, authority in authorities:
                match = re.search(r"^## Revised translation pass\s*\n(.*?)(?=^## Decision|\Z)", authority, re.S | re.M)
                if match:
                    bodies.append(match.group(1).strip())
            if len(bodies) == len(authorities):
                content = "## Translation\n" + "\n\n".join(bodies)

    translation_lines = []
    active_section = False
    for raw_line in content.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", raw_line)
        if heading:
            active_section = heading.group(1).startswith(("Translation", "Extension"))
            continue
        if active_section:
            translation_lines.append(raw_line)
    if not translation_lines:
        raise ValueError(f"{path} lacks a Translation section")

    lines = []
    skip_metadata_block = False
    for raw_line in translation_lines:
        line = raw_line.strip()
        if not line:
            skip_metadata_block = False
            continue
        if line.startswith("#") or line.startswith(("**Source passage:", "**Continuation:", "**Book ")):
            skip_metadata_block = True
            continue
        if skip_metadata_block:
            continue
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        lines.append(escape(line))
    return lines
