# Comic-size production handoff checklist

This checklist is the release-control companion to the current two-volume
architecture. It records the physical target without implying that the present
proof PDFs are printer-ready.

## Locked working specification

| Control | Current target | Evidence / release condition |
|---|---|---|
| Trim | 6.625 × 10.25 in (168.275 × 260.35 mm) | `scripts/preflight_pdfs.py` reports 477 × 738 pt on interior proofs |
| Format | Two-column hardcover casewrap | `design/typography.md`, `design/cover-specification.md` |
| Interior stock | 80# White Coated, Premium Color | Confirm against the selected printer’s current stock name before upload |
| Interior bleed | 0.125 in where artwork reaches the trim | Every full-bleed plate must include live-area and bleed review |
| Interior color | Color-managed RGB/CMYK workflow selected with printer | Final profile and output intent are still pending |
| Current proof counts | Iliad 372 pages; Odyssey 244 pages | Counts must be frozen before printer-template download |
| Cover | One integrated casewrap spread per volume | Must use the printer-generated template, not an estimated spine |
| Typography | Embedded, licensed Cormorant Garamond family | License lock and final PDF font inspection remain required |

## Release gates

- [ ] A named Greek-fidelity reviewer has signed all 24 books in each volume.
- [ ] A separate literary reviewer has signed Longfellow-derived cadence,
  diction, and narrative beauty for every book.
- [ ] Meter and read-aloud outliers have either been revised or expressly
  waived by the named literary editor.
- [ ] The five current Odyssey density holds (Books 19, 21–24) have been
  expanded and reviewed, or have a documented editorial waiver explaining why
  compression is intentional and faithful.
- [ ] Names, notes, glossary, and source-range references have passed their
  independent audit.
- [ ] Every illustration slot has an approved caption/range, rights record,
  role-accurate credit, and print master; concept-review assets are excluded
  from release exports.
- [ ] Historical Blake material distinguishes Flaxman’s design from Blake’s
  engraving wherever applicable; original supplements are labeled as
  CastaliaInstitute work and never as Blake originals.
- [ ] Final text is locked and both volume PDFs are regenerated from that lock.
- [ ] The printer template is downloaded for the exact trim, binding, stock,
  and page count; its filename, date, dimensions, and spine width are recorded
  in `design/release-manifest.yaml`.
- [ ] Interior and cover PDFs pass structural, font, image, bleed, color, and
  page-count checks; no provisional footer or placeholder remains.
- [ ] A physical proof of each volume has been inspected for gutter loss,
  column readability, grayscale/color reproduction, cover wrap, and spine
  alignment, with corrections recorded before final upload.

## Current state

The working proofs satisfy the comic-size geometry and page-count checks, but
the project is not yet a release artifact. Translation approvals, final art,
printer-specific templates, color/profile controls, and physical proofs remain
open. This distinction is intentional: a clean architecture proof is evidence
of production readiness work, not evidence of publication approval.
