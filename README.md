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
- Produce two 7 × 10 inch hardcover volumes with 80# coated paper and
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
requests.
The latest verified run is recorded in [CI verification](preflight/ci-verification.md).

See [PROJECT.md](PROJECT.md) for the production brief and
[CONTRIBUTING.md](CONTRIBUTING.md) for text, image, and provenance conventions.

The working editorial controls are [the translation charter](text/translation-charter.md),
[the design specification](design/specification.md), and the two
[volume plans](volumes/).

The [illustration placeholder deck](design/illustration-placeholders.md)
assigns every book a source-aware plate slot and a prompt for original or
commissioned artwork; these remain placeholders until exact line ranges,
provenance, rights, and print masters are locked.

Translation status is governed by the [review gates](text/review-gates.md);
All 48 books are currently in review; all six review gates remain pending for every book.
The current approval evidence and remaining review work are summarized in the
[translation review dashboard](design/review-dashboard.md).

The [48-book control ledger](text/translation-status.csv) and
[translation workflow](text/translation-workflow.md) make that status
auditable.

The translation structure gate verifies that every non-outline ledger row has
its manuscript file, source passage, translation section, decision log, and
appropriate unresolved-review warning.

`ruby scripts/preflight_review_packets.rb` verifies that all forty-eight
editorial packets exist and that each packet's source-map intervals are
contiguous through its canonical Greek endpoint.

`python3 scripts/preflight_layout.py` verifies the 7 × 10 inch proof geometry
and confirms that representative rendered pages contain text in both columns.

Book 1 source notes for the [*Iliad*](text/iliad/book-01-notes.md) and
[*Odyssey*](text/odyssey/book-01-notes.md) record open Greek-fidelity questions
behind the current drafts.

Rendered-page traceability is maintained in the [page map](design/page-map.csv)
under the rules in [page-map-rules.md](design/page-map-rules.md).

The provisional [release manifest](design/release-manifest.yaml) records the
current development state, printer target, pending locks, and proof classes.
PDF geometry and release-font requirements are checked by
`scripts/preflight_pdfs.py`; the tracked PDFs remain architecture samples until
the full-volume and cover gates are complete.

The [hardcover cover specification](design/cover-specification.md) records the
custom-template dependency, casewrap safety rules, and one-page cover-spread
requirements for each volume.

The [font lock](design/font-lock.md) records the redistributable Cormorant
Garamond files, OFL 1.1 license, checksums, and proof typography settings.

The [cover design proof contract](design/cover-proof.md) defines the
template-dependent casewrap workflow and keeps the current cover studies
explicitly separate from release-ready Lulu cover PDFs.

The [shared glossary](text/glossary.md) records recurring Homeric terms and
translation choices. Image records include role-level attribution for
designer, artist, and engraver.

The active Greek editions and their reproducibility state are recorded in the
[source lock](text/source-lock.md); this separates byte-pinned Iliad drafting
text from the catalog-locked Odyssey record pending a byte-level snapshot.

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
test the 7 × 10 page architecture and are samples, not release PDFs.

The [historical plate proof](output/pdf/inq-homer-historical-plate-proof.pdf)
tests role-level captions for acquired Flaxman/Blake and Flaxman/Piroli scans.

The deterministic [volume-proof assembly contract](design/volume-proof.md)
and the two assembled [Iliad volume proof](output/pdf/inq-homer-iliad-volume-proof.pdf)
and [Odyssey volume proof](output/pdf/inq-homer-odyssey-volume-proof.pdf)
demonstrate the complete 24-book interior architecture while the editorial and
production locks remain in development.
