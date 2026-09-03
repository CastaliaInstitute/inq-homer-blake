# Release-readiness control sheet

**Edition:** CastaliaInstitute / Homer–Blake-informed two-volume set  
**Audit date:** 2026-09-03  
**Format:** comic trim, 6.625 × 10.25 in; two columns; hardcover; 80# white coated interior

This sheet is the handoff control for the final publication review. A green
automated preflight is evidence that the repository is internally consistent;
it is not a substitute for a named human reviewer, a printer specification,
or a physical proof.

## Verified in the repository

| Area | Evidence | Current result |
|---|---|---|
| Source coverage | `design/collation-coverage.md`; source-lock and Greek-coverage preflights | All 48 books have contiguous source authority |
| Translation completeness | `ruby scripts/preflight_translation_completeness.rb`; `scripts/preflight_translation_density.rb`; `design/translation-expansion-plan.md` | All 48 source authorities reach their endpoints; the density screen records provisional holds and the expansion plan makes each hold actionable |
| Accessible reading copies | `output/text/inq-homer-iliad.txt`, `output/text/inq-homer-odyssey.txt` | 24 books in each export; preflight passed |
| Interior architecture | `output/pdf/inq-homer-iliad-volume-proof.pdf`, `output/pdf/inq-homer-odyssey-volume-proof.pdf` | Architecture proofs complete at 477 × 738 pt; final locked-text exports still pending |
| Pagination | `design/release-manifest.yaml` | Iliad 350 pages; Odyssey 146 pages |
| Cover studies | `output/pdf/*cover-design-proof.pdf`; `design/cover-proof.md` | Single integrated 1098 × 846 pt studies; printer template and final spine remain pending |
| Image provenance | `design/plate-manifest.csv`, `design/asset-checksums.csv`, `design/provenance-audit.md`, `design/blake-homer-source-register.md` | Historical Flaxman/engraver roles, primary collection corroboration, original non-Blake credits, and byte-level asset checksums recorded |
| Production snapshot | `design/preflight-report.md` | Deterministic handoff summary of current proofs, coverage, provenance, and release blockers |
| Review governance | `scripts/preflight_review_packets.rb` and all 48 packets | A gate cannot be recorded as passed without a named reviewer and review date |
| Placeholder program | `design/illustration-placeholders.md` | 48 book slots defined; current candidates remain concept-review |
| Typography | `design/font-lock.md`, `design/typography.md` | Architecture font evidence recorded; final license lock pending |
| Automation | `.github/workflows/editorial-quality.yml` | Editorial Quality CI passing on the latest pushed commit |

## Required human and production signoffs

These are intentionally still open. They must be completed and dated before
the release manifest can move beyond `development`:

1. A named Greek-fidelity reviewer compares every book against the pinned Greek
   source and records omissions, additions, names, numbers, agency, and spatial
   sense.
2. A separate literary reviewer assesses beauty, Longfellow-derived cadence,
   diction, image precision, repetition, and read-aloud flow.
3. A meter reviewer resolves the screening outliers or documents intentional
   variation; the syllable report alone is not a prosody approval.
4. A notes/glossary reviewer checks proper names, cultural notes, and editorial
   interventions against the source record.
5. An art director selects or rejects each plate candidate, locks its exact
   passage and caption, and records final creator and rights language. No
   generated concept may be presented as a William Blake work.
6. Production locks the licensed fonts, printer color profile, bleed, cover
   template, binding, paper specification, and final spine widths from the
   printer’s current template.
7. The final interiors and covers are exported from locked text and art, then
   checked with PDF geometry, image/profile, overprint, font-embedding, and
   trim-safety inspection.
8. A physical or printer proof is inspected for ink density, coated-stock
   contrast, registration, trim, gutter, folios, cover wrap, and spine text;
   corrections are recorded and the proof is dated.

## Promotion rule

Do not mark a book `approved`, a plate `final`, or a PDF `release` until its
named signoff and evidence are present. Do not calculate a production spine
from the architecture-proof count alone. The current PDFs are valuable working
proofs, but the edition remains a controlled editorial prototype until the
items above are closed.
