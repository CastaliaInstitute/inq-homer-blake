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

Full-page plates use the 7 × 10 inch trim with 0.125 inch bleed when artwork
reaches the edge. A plate page must carry its source type in the production
manifest even when the printed caption is intentionally minimal. Historical
and generated images must never share an undifferentiated credit line.

## Current proof lock

- Verse: Cormorant Garamond Regular, 11.2 pt / 14.6 pt leading
- Book opener: Cormorant Garamond SemiBold, 19 pt / 23 pt leading
- Volume title: Cormorant Garamond SemiBold, 27 pt / 31 pt leading
- Supporting text: Cormorant Garamond Italic or Regular, 8.7–11 pt
- Page trim: 504 × 720 pt; text margins: 0.72 in outer/inner and 0.75 in top
- Folio rule: 0.48 in from page bottom; folio baseline 0.31 in from bottom

These values describe the reproducible architecture proof. Final approved
lineation, notes, plates, and printer profile may require controlled page-break
adjustments without changing the type license lock.

## Lock before final layout

The production editor must record the selected typefaces, versions, licenses,
point sizes, leading, margins, folio position, and color profile in the release
manifest before either volume is marked `laid-out`.
