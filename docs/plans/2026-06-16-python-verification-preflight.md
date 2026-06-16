# Python Verification Preflight

## Status: In Progress

## Context

The maintained verification surface requires Python 3, but `Makefile` hard-
codes `python3` for unittest discovery while launching the baseline checker by
its independent executable shebang. Contributors therefore cannot select one
compatible interpreter for the full gate, and a missing or incompatible
command fails without a repository-owned diagnostic.

The deployed application remains a legacy Python 2 App Engine application.
This plan changes only the modern offline verification runtime; it does not
claim or attempt a deployment-runtime migration.

## Prioritized Engineering Tasks

1. Make the complete offline verification gate use one explicit, configurable,
   fail-fast Python 3 command.
2. Build a provider replacement plan for retired Picasa and Instagram APIs only
   when owner-managed endpoints, credentials, and a deployable runtime exist.
3. Plan the Python 2 App Engine migration from runtime and provider evidence
   rather than mixing it into narrow security-boundary changes.

This plan implements item 1 because it affects every maintained test and is
fully verifiable without private providers or App Engine.

## Objectives

- Define one Make-level Python command with a `python3` default.
- Add a repository-owned preflight that rejects a missing command or non-
  Python-3 runtime with actionable diagnostics.
- Run both the baseline checker and unittest discovery through the selected
  interpreter while preserving location-independent Make behavior.
- Document the supported interpreter override and distinguish verification
  Python 3 from the unchanged deployment Python 2 runtime.
- Add static and behavioral contracts for propagation, preflight behavior,
  invocation ownership, documentation, and completed evidence.

## Scope

- Update `Makefile`, `scripts/check-baseline.py`, `README.md`, `AGENTS.md`,
  `VISION.md`, and `CHANGES.md`.
- Add a small POSIX-shell preflight helper and extend this plan's completed
  evidence.
- Do not change application Python, App Engine configuration, provider
  contracts, dependencies, credentials, templates, or hosted permissions.

## Verification

- Run POSIX shell syntax validation for the preflight helper.
- Run all four Make aliases from the repository root.
- Run `make check` from an external working directory.
- Run the gate through an explicit compatible Python command override.
- Prove missing and non-Python-3 commands fail with intended diagnostics.
- Run the full characterization suite under the selected interpreter.
- Reject isolated hostile mutations covering propagation, preflight behavior,
  checker ownership, documentation, and plan evidence.
- Audit exact paths, generated caches, credential-like values, dependency and
  workflow drift, conflict markers, file modes, and whitespace.

## Runtime Boundary

No App Engine deployment, private `const.py`, provider credentials, live
provider request, browser route, or production integration is executed or
claimed. The `runtime: python27` deployment declaration remains unchanged.
