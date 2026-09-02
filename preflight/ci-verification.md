# Continuous-integration verification

The `Editorial quality` workflow runs on every push and pull request. It
currently executes the manifest-header check, CSV shape check, translation
ledger check, provenance-field check, prompt-file check, image-file check, and
resolution/status preflight.

## Verified run

- Commit: `1c7c4ea`
- Result: success
- Run: [GitHub Actions run 33620672218](https://github.com/CastaliaInstitute/inq-homer-blake/actions/runs/33620672218)
- Verified: 2026-09-02

The workflow's success proves the repository controls are executable in the
macOS CI environment. It does not certify the literary quality of drafts, the
physical quality of a printed proof, or the release readiness of either volume.
