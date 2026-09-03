# Greek source coverage control

`text/source-coverage.csv` is the current machine-generated coverage ledger
for the forty-eight books. It is built from the exact Greek files and hashes in
`text/source-lock.md`:

```sh
python3 scripts/build_source_coverage.py
```

The builder verifies both locked SHA-256 digests, parses Books 1–24 from each
XML edition, and compares every ledger range with the canonical final Greek
line number. The `line_collation` field records
`complete-working-authority` when the repository's revised collation files
cover the entire canonical range. The repository now contains such authority
files for all 48 books; this provides coverage evidence but does not advance
any Greek-fidelity, narrative, verse, diction, notes, or production review
gate.
A manuscript file and a passing architecture proof do not, by themselves,
certify approval.

This control is intentionally conservative: it makes the remaining editorial
work visible instead of allowing condensed working passages to be mistaken for
release translations.
