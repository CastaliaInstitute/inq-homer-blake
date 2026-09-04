# Current production preflight report

This report is generated from the tracked proofs and manifests. It is a
handoff snapshot, not a release certificate; all human and printer gates
must still be closed in `design/release-readiness.md`.

## Edition target

- Trim: 6.625 × 10.25 inches (comic size), with BookVault's provisional 168 × 260 mm candidate route documented separately
- Interior: two columns, hardcover, 80# White Coated, Premium Color target
- Cover studies: one-page integrated casewrap spreads; printer-specific template required after page-count lock

## Proof inventory

| Artifact | Pages | Page size | Encryption |
|---|---:|---|---|
| Iliad interior proof | 398 | 477 x 738 pts | no |
| Odyssey interior proof | 282 | 477 x 738 pts | no |
| Iliad BookVault prepress interior | 320 | 493.228 x 754.016 pts | no |
| Odyssey BookVault prepress interior | 224 | 493.228 x 754.016 pts | no |
| Iliad cover study | 1 | 1098 x 846 pts | no |
| Odyssey cover study | 1 | 1098 x 846 pts | no |

## Coverage and provenance

- Translation ledger: 48 books; all remain under review.
- Reader-facing density screen: 3 provisional holds; see `design/translation-density-report.md`.
- Architecture page map: 680 traced pages.
- Plate manifest: 55 records; all concept/source-review, none final.
- Iliad print-review art: 24 checksum-bound 2055 × 3142 / 300-PPI sRGB derivatives; human approval pending.
- Odyssey print-review art: 24 checksum-bound 2055 × 3142 / 300-PPI sRGB derivatives; human approval pending.
- BookVault source lock: 0 stale manuscript reference(s); candidate hashes match current manuscript sources.
- Asset checksums: `design/asset-checksums.csv`, rebuilt in CI.
- Font evidence: `design/font-lock.md`; Cormorant Garamond OFL 1.1 files tracked.

## Release blockers

1. Named independent Greek-fidelity review for all 48 books.
2. Separate literary, meter, and notes/glossary approvals.
3. Art-direction selection, passage/caption locks, and rights confirmation.
4. Final printer profile, cover templates, spine widths, and binding lock.
5. Rebuild the stale BookVault candidates after text lock, then run PDF, trim, profile, overprint, font, and source-hash checks.
6. Physical or printer proof inspection and dated correction record.
