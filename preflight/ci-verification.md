# Continuous-integration verification

The `Editorial quality` workflow runs on every push and pull request. It
currently executes the manifest-header check, CSV shape check, translation
ledger check, illustration-placeholder coverage check, provenance-field check,
prompt-file check, image-file check, duplicate-record check, review-packet
coverage check, read-aloud coverage check, source-lock check, translation
structure check, PDF geometry/layout checks, accessible-export check, and
resolution/status preflight.

## Verified run

- Commit: `10dcafc`
- Result: success
- Run: [GitHub Actions run 33723131558](https://github.com/CastaliaInstitute/inq-homer-blake/actions/runs/33723131558)
- Verified: 2026-09-03

The workflow's success proves the repository controls are executable in the
macOS CI environment. It does not certify the literary quality of drafts, the
physical quality of a printed proof, or the release readiness of either volume.
