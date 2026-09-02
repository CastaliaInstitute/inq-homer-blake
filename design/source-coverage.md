# Greek source coverage control

`text/source-coverage.csv` is the current machine-generated coverage ledger
for the forty-eight books. It is built from the exact Greek files and hashes in
`text/source-lock.md`:

```sh
python3 scripts/build_source_coverage.py
```

The builder verifies both locked SHA-256 digests, parses Books 1–24 from each
XML edition, and compares every ledger range with the canonical final Greek
line number. The `line_collation` field remains `pending` until a translator or
reviewer records line-level English coverage and decisions in the control
ledger. The repository now contains source-collated authority files covering
all 48 books; those files provide coverage evidence but do not advance any
Greek-fidelity, narrative, verse, diction, notes, or production review gate.
A manuscript file and a passing architecture proof do not, by themselves,
certify approval.

This control is intentionally conservative: it makes the remaining editorial
work visible instead of allowing condensed working passages to be mistaken for
release translations.
