# Python Verification Preflight

## Status: Completed

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

## Work Completed

- Added a POSIX-shell Python 3 preflight with a `python3` default, a supported
  `PYTHON` override, and actionable missing-command and major-version errors.
- Routed the baseline checker and both unittest discovery invocations through
  the selected interpreter while preserving location-independent Make gates.
- Added checker contracts for helper behavior, Make propagation, checker/test
  ownership, synchronized guidance, and completed evidence.
- Documented the distinction between Python 3 offline verification and the
  unchanged Python 2 App Engine deployment runtime.

## Verification Completed

- POSIX shell syntax and in-memory Python compilation passed.
- All four Make aliases passed from the repository root with Python 3.12.8;
  the complete 25-test characterization suite passed on each applicable gate.
- `make check` passed from the repository root and external working directory.
- The explicit compatible Python command override passed using the resolved
  Python 3 executable path.
- The missing-command and non-Python-3 preflights failed early with their
  intended actionable diagnostics.
- Nine isolated hostile mutations were rejected for the Make default, helper
  propagation, checker ownership, test ownership, command lookup, major-version
  comparison, diagnostic, guidance, and plan-status contracts.
- Exact diff, generated-cache, credential-like value, dependency/workflow
  drift, conflict-marker, file-mode, and whitespace audits passed.
- No App Engine, private configuration, provider credential, live provider,
  browser, or production integration was executed or claimed.
