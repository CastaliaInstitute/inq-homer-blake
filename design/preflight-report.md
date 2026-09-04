# Current production preflight report

This report is generated from the tracked proofs and manifests. It is a
handoff snapshot, not a release certificate; all human and printer gates
must still be closed in `design/release-readiness.md`.

## Edition target

- Primary production trim: standard US comic size, 6.625 × 10.25 in (477 × 738 pt)
- BookVault 168 × 260 mm candidates are alternate prepress studies, not the primary release geometry
- Primary interior: source-line-preserving two-column verse, hardcover, 80# White Coated, Premium Color target
- Cover studies: one-page integrated casewrap spreads; printer-specific template required after page-count lock

## Proof inventory

| Artifact | Pages | Page size | Encryption |
|---|---:|---|---|
| Iliad interior proof | 398 | 477 x 738 pts | no |
| Odyssey interior proof | 282 | 477 x 738 pts | no |
| Iliad BookVault prepress interior | 360 | 493.228 x 754.016 pts | no |
| Odyssey BookVault prepress interior | 250 | 493.228 x 754.016 pts | no |
| Iliad cover study | 1 | 1098 x 846 pts | no |
| Odyssey cover study | 1 | 1098 x 846 pts | no |

## Coverage and provenance

- Translation ledger: 48 books; all remain under review.
- Reader-facing density screen: 3 provisional holds; see `design/translation-density-report.md`.
- Architecture page map: 680 traced pages.
- Plate manifest: 56 records; all concept/source-review, none final.
- Iliad print-review art: 24 checksum-bound 2055 × 3142 / 300-PPI sRGB derivatives; human approval pending.
- Odyssey print-review art: 24 checksum-bound 2055 × 3142 / 300-PPI sRGB derivatives; human approval pending.
- Raster cover studies: HOLD; both contain inaccurate A.Longfellow translator and A.Blake illustrator credits and must not ship.
- BookVault source lock: 0 stale manuscript reference(s); candidate hashes match current manuscript sources.
- BookVault PDF manifest lock: 0 checksum mismatch(es); PDF hashes match the shared manifest.
- Asset checksums: `design/asset-checksums.csv`, rebuilt in CI.
- Font evidence: `design/font-lock.md`; Cormorant Garamond OFL 1.1 files tracked.

## Release blockers

1. Named independent Greek-fidelity review for all 48 books.
2. Separate literary, meter, and notes/glossary approvals.
3. Art-direction selection, passage/caption locks, and rights confirmation.
4. Replacement cover art with accurate built-in author, translator, and illustrator/artist credits.
5. Exact comic-size printer route, final profile, cover templates, spine widths, and binding lock.
6. Rebuild any stale BookVault candidates after text lock, then run PDF, trim, profile, overprint, font, and source-hash checks.
7. Authoritative EPUBCheck plus deterministic two-build comparison.
8. Physical or printer proof inspection and dated correction record.
