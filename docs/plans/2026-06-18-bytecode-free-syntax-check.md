---
title: "fix: Keep syntax checks bytecode-free"
type: fix
date: 2026-06-18
status: completed
---

# fix: Keep syntax checks bytecode-free

## Summary

Make the maintained Python syntax check honor bytecode-disabled validation so
`make check` can run without leaving `__pycache__` or `.pyc` artifacts in the
repository.

## Problem Frame

`scripts/check-baseline.py` calls `py_compile.compile` for each maintained
Python source. That API writes bytecode even when the caller sets
`PYTHONDONTWRITEBYTECODE=1`, so otherwise clean root and external-directory
gates repopulate eleven generated files across three cache directories.

## Requirements

- R1. Syntax validation must still reject invalid maintained Python source.
- R2. The baseline checker must not write bytecode when invoked with bytecode
  writes disabled.
- R3. A regression must detect both a return to `py_compile` and any other
  checker behavior that writes through a redirected Python cache prefix.
- R4. The root and external-directory gates must retain all characterization
  coverage and leave the worktree artifact-free.

## Implementation

- Compile source text in memory with Python's built-in `compile` function and
  report `SyntaxError` failures through the existing failure accumulator.
- Add a subprocess regression that runs the checker with
  `PYTHONDONTWRITEBYTECODE=1` and an isolated `PYTHONPYCACHEPREFIX`, then proves
  the redirected cache directory remains empty.
- Extend the static baseline contract for the helper, regression, and completed
  plan evidence; record the user-visible maintenance change in `CHANGES.md`.

## Scope Boundaries

- No application runtime, App Engine configuration, provider behavior,
  dependencies, workflow matrix, or credentials change.
- Normal Python behavior outside the maintained checker is unchanged.
- Live providers and deployment remain outside this offline validation task.

## Verification Completed

- The focused no-bytecode subprocess regression passed and the complete suite
  passed all 31 characterization tests.
- Bytecode-disabled `make check` passed from the repository root and from
  `/tmp`, preserving the location-independent gate.
- The subprocess checker's redirected cache directory remained empty, and the
  final repository artifact scan found no `__pycache__` directory or `.pyc`
  file.
- Six isolated hostile mutations were rejected: restoring `py_compile`,
  removing in-memory compilation, removing cache-prefix isolation, weakening
  the empty-cache assertion, reverting plan status, and deleting required
  verification evidence.
- No App Engine deployment, private configuration, provider credential, or
  live provider request was executed or claimed.
