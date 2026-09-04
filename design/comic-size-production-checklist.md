# Comic-size production handoff checklist

This checklist is the release-control companion to the current two-volume
architecture. It records the physical target without implying that the present
proof PDFs are printer-ready.

## Locked working specification

| Control | Current target | Evidence / release condition |
|---|---|---|
| Trim | Exact 6.625 × 10.25 in comic size | Architecture proofs declare 477 × 738 pt; BookVault candidates are alternate 168 × 260 mm prepress studies |
| Format | Two-column line-preserving verse; hardcover casewrap | Confirm the selected printer’s current hardcover option and maximum spine before activation |
| Interior stock | 80# White Coated, Premium Color target | Confirm the printer’s current stock name before upload |
| Interior bleed | 3 mm on all sides; 174 × 266 mm MediaBox | Validator checks every page and every full-page plate |
| Interior color | Color-managed RGB/CMYK workflow selected with printer | Final profile and output intent are still pending |
| Current BookVault alternate counts | Iliad 360 pages; Odyssey 250 pages | Alternate candidates only; comic-size architecture proof counts remain primary until final printer lock |
| Cover | One-page integrated casewrap spread on the printer’s exact template | Must use the printer-generated template, not an estimated spine |
| Typography | Embedded, licensed Cormorant Garamond family | License lock and final PDF font inspection remain required |

## Release gates

- [ ] A named Greek-fidelity reviewer has signed all 24 books in each volume.
- [ ] A separate literary reviewer has signed Longfellow-derived cadence,
  diction, and narrative beauty for every book.
- [ ] Meter and read-aloud outliers have either been revised or expressly
  waived by the named literary editor.
- [ ] The two current Odyssey density holds (Books 22–23) have been
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
- [ ] Interior and cover PDFs pass structural, line-wrap, font, image, bleed, color, and
  page-count checks; no provisional footer or placeholder remains.
- [ ] A physical proof of each volume has been inspected for gutter loss,
  column readability, grayscale/color reproduction, cover wrap, and spine
  alignment, with corrections recorded before final upload.

## Current state

The BookVault candidates use the required exact trim, and the Odyssey file has
been revalidated after the current Book 21 revision. Legacy comic-size proofs do
not satisfy the exact-trim production target. None is yet a
release artifact. Translation approvals, final art, printer-specific covers,
color/profile controls, stock confirmation, and physical proofs remain open.
This distinction is intentional: a clean prepress candidate is evidence of
production engineering, not evidence of publication approval.
