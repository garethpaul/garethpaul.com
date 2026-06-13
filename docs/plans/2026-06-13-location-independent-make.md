---
title: Location-Independent Legacy API Verification
date: 2026-06-13
status: planned
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

Pending implementation.

## Verification Completed

Pending implementation and validation. Run `make check` before completion.
