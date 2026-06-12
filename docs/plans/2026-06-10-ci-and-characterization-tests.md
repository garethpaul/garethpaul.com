# CI And Characterization Tests

status: completed

## Context

The portfolio remediation plan calls for lightweight CI and characterization
tests before any larger App Engine runtime decision. The repository already has
a static baseline, but the guard behavior was only enforced through source
string checks and local commands.

## Completed Scope

- Added a GitHub Actions workflow that runs `make check` on Python 3.
- Added dependency-free characterization tests for private endpoint URL
  validation, Instagram pagination/token handling, and Picasa entry shape
  parsing.
- Updated `make test` and `make check` so the behavior tests run locally and in
  CI.
- Extended the static baseline and docs so CI and characterization coverage stay
  visible.

## Verification

- `make test`
- `make check`
- `git diff --check`
