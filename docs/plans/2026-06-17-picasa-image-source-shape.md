---
title: Picasa Image Source Shape
type: reliability
status: planned
date: 2026-06-17
execution: code
---

# Picasa Image Source Shape

## Problem

`picasa_entry_src` returns any `content.src` value. Truthy provider objects,
arrays, booleans, or numbers can therefore enter the JSON image list even
though downstream rendering expects URL text.

## Priorities

1. Accept only Python 2/3-compatible text values for Picasa image sources.
2. Preserve valid ASCII and Unicode source strings while normalizing malformed
   provider values to no image.
3. Protect the handler output, compatibility branch, documentation, and plan
   evidence with focused and mutation-sensitive contracts.

## Implementation

- `picasa.py`: define the repository's existing Python 2/3 text compatibility
  tuple and use it before returning `content.src`.
- `tests/test_integration_guards.py`: cover non-text truthy values and valid
  Unicode image sources.
- `scripts/check-baseline.py`: enforce the compatibility branch, helper guard,
  tests, guidance, and completed verification evidence.
- `AGENTS.md`, `README.md`, `SECURITY.md`, `VISION.md`, and `CHANGES.md`: record
  the provider source-shape boundary.

## Validation

- Run focused provider tests, the full Python 3 suite, Python 2 compilation,
  and repository-root/external-directory `make check` gates.
- Reject isolated mutations that remove the type guard, weaken it to truthiness,
  remove malformed or Unicode coverage, or reopen this plan.
- Audit syntax, diff, generated artifacts, and changed-line credential patterns.

## Risks

- This normalizes malformed provider entries to no image instead of emitting
  non-text JSON values; valid text behavior remains unchanged.
- Live retired Picasa responses and App Engine deployment remain outside local
  verification.
