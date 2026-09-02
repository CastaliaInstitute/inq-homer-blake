# Greek source lock

This file records the digital source resolution used for active translation
drafts. It is a provenance aid, not a claim that any book has passed the
Greek-fidelity gate.

## Iliad

- CTS edition: `urn:cts:greekLit:tlg0012.tlg001.perseus-grc2`
- Edition: D. B. Monro and T. W. Allen, *Homeri Opera*, Oxford, 1920
- Repository: [PerseusDL/canonical-greekLit](https://github.com/PerseusDL/canonical-greekLit)
- Pinned commit: `ac0bc60033f1f83990a5cf7f1e7fc2e0423e381a`
- Raw XML: `data/tlg0012/tlg001/tlg0012.tlg001.perseus-grc2.xml`
- SHA-256: `15ab2da1201d6160db741e7806f12667f692d47e5884e216c3bd12b08efa4ce8`
- Active drafts: Iliad Books 1–24

## Odyssey

- CTS edition: `urn:cts:greekLit:tlg0012.tlg002.perseus-grc2`
- Edition: A. T. Murray, *The Odyssey*, 1919
- Repository: [PerseusDL/canonical-greekLit](https://github.com/PerseusDL/canonical-greekLit)
- Pinned commit: `ac0bc60033f1f83990a5cf7f1e7fc2e0423e381a`
- Raw XML: `data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml`
- SHA-256: `246f17cc2e9c3f4e8b97fe7d6fcf56dbc4f34f215d9b1447b2878a6152e0656a`
- Retrieval URL: `https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/ac0bc60033f1f83990a5cf7f1e7fc2e0423e381a/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml`
- Catalog record: [Perseus Catalog Odyssey record](https://catalog.perseus.org/catalog/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-grc1)
- Citation service: [Scaife Odyssey library record](https://atlas.perseus.tufts.edu/nodes/urn%3Acts%3AgreekLit%3Atlg0012.tlg002%3A/)
- Snapshot status: byte-identified; source XML is fetched on demand and verified against the hash above
- Active drafts: Odyssey Books 1–24

## Review rule

Before a draft advances from `draft`, the reviewer must record the exact
Greek citation span, consulted apparatus, adopted readings, and date of
collation in that book's source notes.

## Verification command

```sh
curl -L --fail --silent --show-error \
  'https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/ac0bc60033f1f83990a5cf7f1e7fc2e0423e381a/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml' \
  | shasum -a 256
```

The resulting digest must equal the locked SHA-256 above before collation.
