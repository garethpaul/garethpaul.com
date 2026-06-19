---
title: Instagram Pagination URL Shape
date: 2026-06-16
status: completed
execution: code
---

## Context

`instagram_page` normalizes malformed pagination and media containers, but it
returns `pagination.next_url` without validating that the value is text. A
truthy list, object, number, or boolean therefore reaches `instagram_json`,
where URL parsing raises instead of treating the malformed optional pagination
field as absent.

## Priority

This is the highest-value remaining deterministic provider-schema gap because
it is reachable from untrusted provider JSON, can turn a recoverable malformed
optional field into a request failure, and can be corrected without changing
valid pagination, bearer-token handling, deployment configuration, or private
credentials.

## Plan

1. Add one Python 2/3-compatible text-type tuple and normalize non-text
   `next_url` values to `None` inside `instagram_page`.
2. Extend characterization coverage for valid text values and malformed
   truthy scalar/container values while preserving media-list behavior.
3. Add a mutation-sensitive baseline contract for the text guard, focused
   tests, guidance, changelog, and completed plan evidence.
4. Run the focused suite, all Make gates, external-directory validation,
   isolated hostile mutations, and final diff/artifact/secret audits.
5. Push the exact branch, open a stacked pull request against the Python
   preflight branch, and take one bounded hosted/security snapshot.

## Non-Goals

- Replacing retired Instagram or Picasa APIs.
- Migrating the Python 2 App Engine runtime.
- Exercising live provider endpoints or adding credentials.
- Changing valid Instagram pagination destinations or bearer-token transport.

## Verification Required

- Focused and full characterization tests pass under the maintained Python 3
  verification command.
- `make check`, `make lint`, `make test`, and `make build` pass, including an
  absolute Makefile invocation from an external directory.
- Isolated mutations that remove the text guard, accept arbitrary truthy
  values, remove malformed-value coverage, or stale the plan evidence fail.
- The final intended diff passes syntax, whitespace, artifact, credential,
  conflict-marker, file-mode, and upstream-alignment audits.

## Work Completed

- Added a Python 2/3-compatible text-type tuple and normalized non-text
  `pagination.next_url` values to `None` while preserving valid current-page
  media.
- Added focused characterization and static contracts for truthy malformed
  pagination URL values, guidance, and completed verification evidence.

## Verification Completed

- The focused and complete characterization tests passed: the integration file
  ran 24 tests and the complete suite ran 26 tests on Python 3.
- Python 3 compilation passed for the changed checker, source, and test, and
  Python 2.7 compilation passed for the production `instagram.py` module.
- All four Make gates passed in the isolated baseline mirror and again in the
  final worktree.
- The external-directory Make gate passed through the absolute Makefile path.
- The text-type guard mutation failed after restoring the unvalidated direct
  pagination return.
- The arbitrary-truthy-value mutation failed after replacing the type check
  with a truthiness check.
- The focused-test contract mutation failed after renaming the malformed URL
  characterization.
- The Python 2 text compatibility mutation failed after reducing the accepted
  type tuple to Python 3 `str` only.
- The plan-status mutation failed after restoring an active status.
- The plan-evidence mutation failed after removing the text-guard mutation
  result.
- Diff, generated-artifact, credential, conflict-marker, file-mode, and exact
  upstream audits completed before commit.
