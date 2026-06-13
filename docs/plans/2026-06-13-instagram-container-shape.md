---
title: Instagram Container Shape
date: 2026-06-13
status: planned
execution: code
---

## Context

Instagram responses now require a top-level JSON object, but the handler still
chains `.get` through `pagination` and assumes each page's `data` value is a
list. A non-object pagination container raises before URL validation, while a
string or object media container can fail or concatenate unintended values.

## Priority

This is the highest-value remaining isolated provider-schema guard because both
the first page and optional second page cross the same retired Instagram API
boundary. Normalizing malformed nested containers can preserve the existing
JSON list response without changing credentials, pagination host validation,
timeouts, response limits, or valid media ordering.

## Prioritized Backlog

1. Accept `pagination` only as an object and media `data` only as a list.
2. Treat missing or malformed nested containers as no next page and an empty
   media list.
3. Apply the same shape boundary to the initial and optional second page.
4. Add focused characterization and hostile-mutation contracts plus repository
   guidance.
5. Keep map, geocode, and weather leaf-schema validation as separate work.

## Implementation

- Add a small Instagram page-container helper that returns a safe next URL and
  media list.
- Route both page reads through the helper before pagination or concatenation.
- Extend characterization tests and the static baseline with malformed
  pagination, malformed media-list, helper-use, and completed-plan contracts.
- Update README, SECURITY, VISION, CHANGES, and AGENTS guidance.

## Verification Plan

- Run focused integration tests, all characterization tests,
  `scripts/check-baseline.py`, all four Make gates, Python compilation,
  workflow parsing, `git diff --check`, and intended-file artifact and secret
  scans.
- Remove the pagination-object guard, remove the media-list guard, and bypass
  the helper for the second page; each hostile mutation must fail.
- Take one bounded exact-head push, pull-request, and code-scanning snapshot
  after push; do not poll.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and verification.
