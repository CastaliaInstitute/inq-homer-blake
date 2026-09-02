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

Run `scripts/validate_manifests.sh` before committing manifest changes.

See [PROJECT.md](PROJECT.md) for the production brief and
[CONTRIBUTING.md](CONTRIBUTING.md) for text, image, and provenance conventions.

The working editorial controls are [the translation charter](text/translation-charter.md),
[the design specification](design/specification.md), and the two
[volume plans](volumes/).
