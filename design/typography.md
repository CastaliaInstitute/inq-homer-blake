# Shared typography and page architecture

This system is shared by both volumes so that the set feels intentional while
each epic retains its own image sequence. The current locked proof face is
Cormorant Garamond, packaged under `assets/fonts/` with its OFL 1.1 license;
the exact files and checksums are recorded in `design/font-lock.md`.

## Hierarchy

| Element | Treatment | Rule |
|---|---|---|
| Volume title | Cormorant Garamond, restrained capitals | Never set over a busy image |
| Book opening | Display face with Arabic book number and Greek letter in metadata | Begin on a recto page where pagination permits |
| Verse | Cormorant Garamond, generous leading, ragged right edge | Preserve line breaks; never justify the poem |
| Notes | Cormorant Garamond Italic/roman, clearly separated from verse | Notes must never be mistaken for translated lines |
| Plate caption | Small roman text with creator role and source type | Place adjacent to image, not inside the art |
| Running furniture | Book number on verso; epic title on recto | Suppress on title, dedication, and plate-only pages |

## Verse page rules

- Keep the translation's lineation stable after copy approval.
- Avoid widows and orphans without changing the poem's wording; adjust page
  breaks or image placement first.
- Keep a minimum of two lines of verse together at a page turn.
- Begin speeches with consistent indentation and quotation treatment.
- Reserve the outer margin for folios and the inner margin for binding safety.

## Plate-page rules

Full-page plates use the primary 6.625 × 10.25 inch comic trim with 0.125 inch bleed when artwork
reaches the edge. A plate page must carry its source type in the production
manifest even when the printed caption is intentionally minimal. Historical
and generated images must never share an undifferentiated credit line.

## Current proof lock

- Verse: Cormorant Garamond Regular, 11.2 pt / 14.6 pt leading
- Book opener: Cormorant Garamond SemiBold, 19 pt / 23 pt leading
- Volume title: Cormorant Garamond SemiBold, 27 pt / 31 pt leading
- Supporting text: Cormorant Garamond Italic or Regular, 8.7–11 pt
- Primary production page trim: 6.625 × 10.25 inches inside a 6.875 × 10.5 inch bleed MediaBox;
  text margins: 0.72 in outer/inner and 0.75 in top
- Folio rule: 0.48 in from page bottom; folio baseline 0.31 in from bottom

The type values describe the reproducible architecture. Existing 477 × 738 pt
PDFs are legacy design proofs, not exact-trim production files. Final approved
lineation, notes, plates, and printer profile may require controlled page-break
adjustments without changing the type license lock.

The primary comic-size architecture uses two verse columns, preserving the
source manuscript's lineation and keeping the requested reading rhythm visible
on the page. The alternate 168 × 260 mm BookVault candidate currently uses one
full-width verse column so each source manuscript line remains one printed line
at 10.5 pt; that alternate builder must fail if any line wraps. Editorial line
breaks are revised transparently in the manuscript, never manufactured by
layout. The BookVault candidate is a prepress engineering study, not authority
for the primary two-column design.

## Lock before final layout

The production editor must record the selected typefaces, versions, licenses,
point sizes, leading, margins, folio position, and color profile in the release
manifest before either volume is marked `laid-out`.
