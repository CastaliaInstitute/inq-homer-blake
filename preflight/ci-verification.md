# Continuous-integration verification

The `Editorial quality` workflow runs on every push and pull request. It
currently executes the manifest-header check, CSV shape check, translation
ledger check, illustration-placeholder coverage check, provenance-field check,
prompt-file check, image-file check, duplicate-record check, review-packet
coverage check, read-aloud coverage check, source-lock check, translation
structure check, multi-line manuscript-duplication check, PDF geometry/layout
checks, accessible-export check, and resolution/status preflight.

## Reference verified run

- Commit: `814ec49`
- Result: success
- Run: [GitHub Actions run 33758774225](https://github.com/CastaliaInstitute/inq-homer-blake/actions/runs/33758774225)
- Verified: 2026-09-03

This is a reference run, not a substitute for checking the workflow attached to
the current commit; GitHub Actions runs again on every push and pull request.

The workflow's success proves the repository controls are executable in the
macOS CI environment. It does not certify the literary quality of drafts, the
physical quality of a printed proof, or the release readiness of either volume.
