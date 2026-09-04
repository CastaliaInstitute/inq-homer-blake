# Release-readiness control sheet

**Edition:** Castalia Institute / Homer two-volume set

**Audit date:** 2026-09-04

**Required format:** standard US comic trim, 6.625 × 10.25 in; 0.125 in bleed; two-column line-preserving verse

**Decision:** **HOLD — neither volume is release-approved.**

A passing build proves only internal consistency. It cannot substitute for
source, literary, art, rights, printer, or physical-proof approval.

## Repository evidence

| Area | Result | Evidence / limitation |
|---|---|---|
| Book and source structure | PASS | 24 ordered books per volume; all 48 source-span authorities reach their canonical endpoint without a ledger gap or overlap. |
| Duplicate screen | PASS | All 48 openings and collation authorities pass repeated-block and adjacent-duplicate checks. This is not an omissions audit. |
| Reader-facing completeness | HOLD | All 48 books now clear the conservative 5.0 words/source-line screen; *Odyssey* Book 23 now screens at 5.01. Every book remains under Greek-fidelity, literary, meter, notes, and human signoff gates. |
| Human editorial gates | HOLD | All 48 books are `review`; all 288 Greek, narrative, verse, diction, notes, and production gate cells remain `pending`. |
| Oral prosody | HOLD | 7,444/12,712 *Iliad* lines (58.6%) and 6,055/8,628 *Odyssey* lines (70.2%) fall in the heuristic 8–12-syllable band; 7,841 outliers remain unreviewed. |
| Accessible text | PASS (provisional) | Two plain-text exports contain Books 1–24 in order and exclude editorial logs. |
| EPUB | HOLD | Deterministic, reflowable, illustration-free private proofs can be built with semantic navigation and fail-closed rights metadata. Authoritative EPUBCheck is not installed locally; final covers are also unresolved. |
| Interior geometry | HOLD | Comic-size architecture proofs are 477 × 738 pt. Separate BookVault candidates validate at exact 168 × 260 mm with 24 full-page plates and embedded fonts; they are alternate prepress candidates, not the primary comic-size edition. |
| Legacy PDFs | HOLD | 477 × 738 pt interiors/web samples and 1098 × 846 pt comic-size cover studies are architecture artifacts, not exact-trim release files. |
| Plates | HOLD | The 48-slot `design/plate-selection-audit.csv` binds exactly one current candidate to every book. All selections remain pending; many sources are upscaled concept art, not native masters. |
| Cover art and credits | HOLD | Both raster front-cover studies visibly miscredit “A.Longfellow” as translator and “A.Blake” as illustrator. They are excluded from editorial EPUBs and cannot be released. |
| Provenance and rights | HOLD | Two historical Met scans have object-level public-domain records with Flaxman/designer and Blake-or-Piroli/engraver roles. Original candidates are documented as CastaliaInstitute work, not William Blake; final plate rights grants and selections remain open. |
| Typography | HOLD | Cormorant Garamond binaries and OFL evidence are present and candidate PDF fonts are embedded; production font/license lock and printer output intent remain unsigned. |
| Reproducible build | HOLD | Build scripts and checksum manifests exist. Current-branch CI, EPUBCheck, final PDF/profile checks, and a clean two-run reproducibility record remain required after text/art lock. |

## Cover artifact audit

| Files | Result | Exact defect |
|---|---|---|
| `assets/covers/epic/{iliad,odyssey}/cover-art.png` | HOLD | Distinct art-only studies (1024 × 1536 and 1009 × 1559); no built-in credits, final provenance/right grant, or full-bleed 300-PPI production master. |
| `assets/covers/epic/{iliad,odyssey}/front-cover.jpg` | HOLD | 2055 × 3142 / 300-PPI derivatives, but both visibly miscredit A.Longfellow and A.Blake. |
| `assets/covers/epic/{iliad,odyssey}/web-cover.webp` | HOLD | 900 × 1376 web derivatives repeat the unsafe built-in credits and are not print masters. |
| `output/pdf/inq-homer-*-cover-design-proof.pdf` | HOLD — corrected provisional | Distinct one-page comic-size casewrap studies now carry Homer, Castalia Institute as translator, and truthful Castalia Institute cover-art credit; placeholder spines and exact printer templates remain unresolved. |

The illustration-free EPUB cover pages are the only currently credit-safe
cover treatment; they are deliberately not represented as final cover art.

## Exact remaining gates

1. Begin independent human approval of all 48 source-collated books, beginning
   with the late Odyssey recognition and reconciliation sequence, then complete
   independent omissions/additions and fidelity reports for all 48 books.
2. Obtain named signoff for all 288 editorial gate cells and resolve/document
   the 7,841 meter-screen outliers through human read-aloud review.
3. Select 48 final plates; lock passage, caption, creator role, rights/license,
   native-resolution master, and printer profile for each.
4. Retire the inaccurate raster cover studies, then adapt the corrected
   provisional proofs to distinct exact printer templates carrying Homer,
   Castalia Institute as translator, and truthful cover-art creator credits.
   Do not invent an ISBN.
5. Lock the exact comic-size printer route, stock, binding, output profile,
   final page counts, generated cover templates, and spine widths.
6. Rebuild from locked sources; pass text, EPUBCheck, PDF box/font/image/profile,
   trim-safety, and reproducibility checks; inspect and date physical proofs.

No artifact may be labeled `release`, `final`, sale-approved, or publicly
distributable until every applicable gate above has evidence.
