# iNQ Homer Blake

An iNQ project to create an illustrated English edition of Homer's
_Iliad_ and _Odyssey_, pairing documented public-domain work by William Blake
with clearly identified original plates where additional visual coverage is
needed.

## Volumes

- `iliad` — _The Iliad_, Homer
- `odyssey` — _The Odyssey_, Homer

## Editorial principles

- Preserve the poems from verified public-domain copy texts.
- Record the translation, edition, and source passage for every excerpt.
- Reproduce Blake's historical work only with full provenance and plate-level
  captions.
- Label newly generated or commissioned images as new work; never present
  them as Blake originals.
- Design to a 7 × 10 inch trim size with print-safe margins and high-resolution
  image assets.

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

See [PROJECT.md](PROJECT.md) for the production brief and
[CONTRIBUTING.md](CONTRIBUTING.md) for text, image, and provenance conventions.
