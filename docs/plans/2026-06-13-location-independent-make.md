---
title: Location-Independent Legacy API Verification
date: 2026-06-13
status: completed
execution: code
---

## Context

The maintained baseline passes from the checkout but fails when the absolute
Makefile is loaded from another working directory. The checker and unittest
discovery commands are resolved relative to the caller instead of the
repository.

## Priority

This is the next isolated reliability gap because local and CI automation
should be able to invoke a checked-out Makefile without first changing
directories. The change must preserve all legacy App Engine, provider,
credential, timeout, response-size, schema, template, and workflow behavior.

## Requirements

- Derive the repository root from `MAKEFILE_LIST`.
- Run checker and unittest commands from that repository root for every Make
  gate.
- Add static contracts for the rooted Makefile, completed plan, external-run
  evidence, and synchronized guidance.
- Add mutation-sensitive verification for root derivation, checker execution,
  unittest execution, plan status/evidence, and documentation drift.
- Keep production Python, templates, dependencies, and workflow files
  unchanged.

## Verification Plan

- Run focused and full characterization tests, `scripts/check-baseline.py`, and
  all four Make gates at repository root.
- Run all four Make gates from /tmp through the absolute Makefile path.
- Reject isolated caller-relative root, checker, unittest, plan-status,
  plan-evidence, and documentation mutations.
- Run Python 3 and Python 2 production-module compilation, workflow parsing,
  `git diff --check`, exact-path review, secret scanning, and artifact checks.

## Non-Goals

- Changing provider requests, credentials, URL validation, timeouts, response
  limits, JSON shape handling, templates, dependencies, or deployment policy.
- Claiming live App Engine routes or private provider integrations without the
  intentionally absent `const.py` and credentials.

## Work Completed

- Derived the repository root from the loaded Makefile and ran checker and
  unittest commands from that root for every gate.
- Extended the Python baseline with rooted-Makefile, completed-plan,
  external-run, and synchronized-guidance contracts.
- Preserved production Python, templates, dependencies, private configuration,
  and workflow files unchanged.

## Verification Completed

- The focused integration file ran 18 tests and the complete suite ran 20 tests.
- All four Make gates (`make lint`, `make test`, `make build`, and `make check`)
  passed at repository root and from /tmp through the absolute Makefile path.
- The root-derivation mutation failed.
- The checker-command mutation failed.
- The unittest-command mutation failed.
- The plan-status mutation failed.
- The plan-evidence mutation failed.
- The documentation mutation failed.
- Python 3 and Python 2 production-module compilation, workflow parsing,
  `git diff --check`, exact intended-path review, added-line secret scanning,
  and generated-artifact inspection passed.
- Live App Engine routes and private provider integrations were unavailable
  without the intentionally absent `const.py` and credentials and are not
  claimed.
