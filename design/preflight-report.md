# Current production preflight report

This report is generated from the tracked proofs and manifests. It is a
handoff snapshot, not a release certificate; all human and printer gates
must still be closed in `design/release-readiness.md`.

## Edition target

- Trim: 6.625 × 10.25 inches (comic size)
- Interior: two columns, hardcover, 80# White Coated, Premium Color target
- Interior page geometry: 477 × 738 points
- Cover studies: one-page integrated casewrap spreads, template-dependent

## Proof inventory

| Artifact | Pages | Page size | Encryption |
|---|---:|---|---|
| Iliad interior proof | 350 | 477 x 738 pts | no |
| Odyssey interior proof | 241 | 477 x 738 pts | no |
| Iliad cover study | 1 | 1098 x 846 pts | no |
| Odyssey cover study | 1 | 1098 x 846 pts | no |

## Coverage and provenance

- Translation ledger: 48 books; all remain under review.
- Reader-facing density screen: 5 provisional holds; see `design/translation-density-report.md`.
- Architecture page map: 591 traced pages.
- Plate manifest: 22 records; all concept/source-review, none final.
- Asset checksums: `design/asset-checksums.csv`, rebuilt in CI.
- Font evidence: `design/font-lock.md`; Cormorant Garamond OFL 1.1 files tracked.

## Release blockers

1. Named independent Greek-fidelity review for all 48 books.
2. Separate literary, meter, and notes/glossary approvals.
3. Art-direction selection, passage/caption locks, and rights confirmation.
4. Final printer profile, cover templates, spine widths, and binding lock.
5. Final locked-text/art exports with PDF, trim, profile, overprint, and font checks.
6. Physical or printer proof inspection and dated correction record.
