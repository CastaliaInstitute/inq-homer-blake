# iNQ Homer Blake

An iNQ project to create a new English translation of Homer in the manner of
Henry Wadsworth Longfellow's translation of Dante's _Divine Comedy_: unrhymed
iambic pentameter, ceremonial diction, and a grave, flowing narrative line.
The two-volume edition will be illustrated with William Blake's historical
work where appropriate, supplemented by clearly identified new plates in
conversation with Blake's visual language.

## Volumes

- `iliad` — _The Iliad_, Homer
- `odyssey` — _The Odyssey_, Homer

## Editorial and production principles

- Translate directly from a verified Greek source while treating Longfellow's
  _Divine Comedy_ as the principal formal and tonal model.
- Preserve Homer's twenty-four-book structure in each epic.
- Record the Greek edition, translation decisions, and source passage for every
  translated section.
- Reproduce Blake's historical work only with full provenance and plate-level
  captions.
- Label newly generated or commissioned images as new work; never present
  them as Blake originals.
- Produce two standard US comic-size hardcover volumes (6.625 × 10.25 in) with 80# coated paper and
  print-safe margins and high-resolution image assets.

## Repository layout

```text
volumes/                 volume-level editorial plans and manifests
assets/source/           scans and source-image records
assets/generated/       generated plate candidates and prompts
assets/processed/        print-ready image derivatives
text/                    normalized text and source metadata
design/                  trim, grid, typography, and color specifications
preflight/               repeatable production checks
scripts/                 repeatable validation and production utilities
```

Run `scripts/validate_manifests.sh` before committing manifest changes and
`scripts/preflight_assets.rb` before promoting an image record to `final`.
These checks also run automatically in GitHub Actions for pushes and pull
requests under `.github/workflows/quality.yml`.
A reference workflow run and its limitations are recorded in [CI verification](preflight/ci-verification.md); the current commit must be checked in GitHub Actions before release.

See [PROJECT.md](PROJECT.md) for the production brief and
[CONTRIBUTING.md](CONTRIBUTING.md) for text, image, and provenance conventions.

The working editorial controls are [the translation charter](text/translation-charter.md),
[the design specification](design/specification.md), and the two
[volume plans](volumes/).

The [illustration placeholder deck](design/illustration-placeholders.md)
assigns every book a source-aware plate slot and a prompt for original or
commissioned artwork; these remain placeholders until exact line ranges,
provenance, rights, and print masters are locked.
The current candidate inventory and prioritized art-selection risks are recorded
in the [illustration curation report](design/illustration-curation-report.md).
The deterministic [plate asset checksum ledger](design/asset-checksums.csv) is
rebuilt in CI from the plate manifest so replacement files cannot silently
change beneath their provenance records.

All 24 books in each volume now have a provisionally selected original
candidate in `design/iliad-plate-selection.csv` and
`design/odyssey-plate-selection.csv`. Run the corresponding
`scripts/prepare_*_print_art.py` builder to rebuild the checksum-bound 2055 ×
3142 pixel, 300-PPI, embedded-sRGB derivatives, and run
`python3 scripts/preflight_homer_print_art.py` to verify their complete source
lineage. These are interpolated placement derivatives for review, not native
masters or approved final art.

`python3 scripts/build_web_previews.py` builds the two web samplers from the
book-owned cover, the selected Book I print-review plate, and the complete
current Book I translation. Their opening order is cover / plate / text, so PDF
page 2 is the standalone plate and page 3 begins the two-column text sampler.
The single plate is not repeated between text pages. Run
`python3 scripts/preflight_web_previews.py` to verify canonical trim, page
counts, image placement, and complete Book I text coverage.

`python3 scripts/build_bookvault_interiors.py` builds the two checksum-bound
BookVault prepress candidates. Each page has a 174 × 266 mm bleed MediaBox and
an exact comic-size TrimBox; each of the 24 books opens with one full-page
2055 × 3142 pixel plate followed by source-line-preserving two-column verse.
The builder rejects any verse line that would wrap at the production measure,
so lineation cannot silently change in PDF layout. The builder stages output
atomically under an exclusive lock and pads an odd final page count. Run
`python3 scripts/validate_bookvault_interiors.py` to verify page boxes, even
page counts, embedded fonts, art checksums, and complete per-book source text.
The generated manifest remains `releaseEligible: false` until named editorial,
illustration, font-license, and physical-proof approvals are recorded.

Because “illustrated by Blake” can obscure the distinction between designer
and engraver, the [Blake–Homer source register](design/blake-homer-source-register.md)
records the primary collection evidence and controlled attribution language.
Historical Homer material is used by documented role; Blake-informed
supplements remain explicitly original and non-Blake.

Translation status is governed by the [review gates](text/review-gates.md);
All 48 books are currently in review; all six review gates remain pending for every book.
The current approval evidence and remaining review work are summarized in the
[translation review dashboard](design/review-dashboard.md).

The physical-edition handoff is controlled by the [production
checklist](design/comic-size-production-checklist.md), which keeps the
comic-size target distinct from alternate 168 × 260 mm BookVault studies
proofs and from final printer-template and physical-proof approval.

The [48-book control ledger](text/translation-status.csv) and
[translation workflow](text/translation-workflow.md) make that status
auditable.

The translation structure gate verifies that every non-outline ledger row has
its manuscript file, source passage, translation section, decision log, and
appropriate unresolved-review warning.

`ruby scripts/preflight_review_packets.rb` verifies that all forty-eight
editorial packets exist and that each packet's source-map intervals are
contiguous through its canonical Greek endpoint.

`ruby scripts/preflight_read_aloud.rb` verifies that all forty-eight books have
an explicitly non-final read-aloud/fidelity review record with human review
held open.

`ruby scripts/preflight_translation_density.rb` screens the reader-facing
Translation sections for material compression against their declared Greek
source ranges. It is a conservative hold mechanism, not proof of literary
quality or Greek fidelity; see the [density report](design/translation-density-report.md)
and the generated [translation expansion plan](design/translation-expansion-plan.md).

`ruby scripts/preflight_illustration_placeholders.rb` verifies that all forty-
eight book slots have unique prompts, exact canonical source ranges, and
provenance direction before any candidate is promoted to final art.

`python3 scripts/preflight_layout.py` verifies the comic-size proof geometry
and confirms that representative rendered pages contain text in both columns.

`python3 scripts/build_meter_report.py` produces a heuristic syllable-band
screen for all 48 working books; it is explicitly screening-only and does not
replace stress analysis or a human read-aloud.
The same command writes a complete [`meter-outliers.csv`](text/meter-outliers.csv)
log for line-level follow-up.

`python3 scripts/preflight_text_exports.py` verifies the structure of both
provisional accessible text exports before handoff.

Book 1 source notes for the [*Iliad*](text/iliad/book-01-notes.md) and
[*Odyssey*](text/odyssey/book-01-notes.md) record open Greek-fidelity questions
behind the current drafts.

Rendered-page traceability is maintained in the [page map](design/page-map.csv)
under the rules in [page-map-rules.md](design/page-map-rules.md).

The complete current-proof traceability pass is recorded in the [provisional
architecture page map](design/architecture-page-map.csv), generated by
`scripts/build_architecture_page_map.py`. It accounts for every page in both
comic-size volume proofs while remaining explicitly non-final.

The provisional [release manifest](design/release-manifest.yaml) records the
current development state, printer target, pending locks, and proof classes.
The deterministic [Iliad text export](output/text/inq-homer-iliad.txt) and
[Odyssey text export](output/text/inq-homer-odyssey.txt) provide accessible
plain-text reading copies; both remain provisional with the translation gates.
Deterministic EPUB 3 editorial proofs can be built with
`python3 scripts/build_epub.py` and checked with `python3 scripts/validate_epub.py`.
Their package metadata and build manifests explicitly prohibit sale and public
distribution while review gates remain open; unapproved plate and cover art is
omitted. The two existing raster cover studies carry inaccurate translator and
illustrator text and are not eligible for packaging or release.
Web samplers can be regenerated with `python3 scripts/build_web_previews.py`;
they contain the cover study, one original concept plate, and complete Book I
text with explicit Longfellow-inspired/Castalia Institute attribution.
PDF geometry and release-font requirements are checked by
`scripts/preflight_pdfs.py`; the tracked PDFs remain architecture samples until
the full-volume and cover gates are complete.

The [hardcover cover specification](design/cover-specification.md) records the
custom-template dependency, casewrap safety rules, and one-page cover-spread
requirements for each volume.

The [font lock](design/font-lock.md) records the redistributable Cormorant
Garamond files, OFL 1.1 license, checksums, and proof typography settings.

The generated [production preflight report](design/preflight-report.md)
consolidates the current proof inventory, comic-size geometry, page-map coverage,
plate provenance, and outstanding release blockers for editorial or printer
handoff.

The [cover design proof contract](design/cover-proof.md) defines the
template-dependent casewrap workflow and keeps the current cover studies
explicitly separate from release-ready Lulu cover PDFs.

The [shared glossary](text/glossary.md) records recurring Homeric terms and
translation choices. Image records include role-level attribution for
designer, artist, and engraver.

The active Greek editions and their reproducibility state are recorded in the
[source lock](text/source-lock.md); both drafting sources are byte-identified
by pinned repository commits and SHA-256 digests, with the Odyssey XML fetched
on demand and verified before collation.

The [Greek source coverage control](design/source-coverage.md) records the
canonical final line for every book and keeps line-level translation collation
explicitly pending until it is actually performed.

The unified [plate manifest](design/plate-manifest.csv) joins historical and
generated plates at the production level, including source type, caption,
credit, dimensions, profile state, and provenance record.

The [provenance audit](design/provenance-audit.md) preserves local checksums
and attribution boundaries for historical Met scans and original concept
plates; `scripts/preflight_provenance.rb` enforces those boundaries in CI.

The first original plate candidate is documented in the
[Apollo prompt record](assets/generated/prompts/iliad-book-01-apollo-v1.md);
it is concept-review only until a print-resolution master is approved.

The first [Iliad Book 1 interior proof](output/pdf/inq-homer-book-1-proof.pdf)
and matching [Odyssey Book 1 interior proof](output/pdf/inq-homer-odyssey-book-1-proof.pdf)
test the comic-size page architecture and are samples, not release PDFs.

The [historical plate proof](output/pdf/inq-homer-historical-plate-proof.pdf)
tests role-level captions for acquired Flaxman/Blake and Flaxman/Piroli scans.

The deterministic [volume-proof assembly contract](design/volume-proof.md)
and the two assembled [Iliad volume proof](output/pdf/inq-homer-iliad-volume-proof.pdf)
and [Odyssey volume proof](output/pdf/inq-homer-odyssey-volume-proof.pdf)
demonstrate the complete 24-book interior architecture while the editorial and
production locks remain in development.
