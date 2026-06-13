---
title: Picasa Feed Container Shape
date: 2026-06-13
status: planned
execution: code
---

## Context

The Picasa proxy now requires a top-level JSON object and safely skips malformed
individual entries, but it still chains `.get` through `feed` and assumes
`feed.entry` is iterable as a list. Provider payloads such as `{"feed": []}`
raise an attribute error, while string or object entry containers can be
silently iterated as unintended data.

## Priority

This is the highest-value remaining isolated provider-schema guard because the
legacy Picasa API is retired and partial or drifted payloads are expected. The
route already defines an empty image-list fallback, so container validation can
preserve that response contract instead of turning provider shape drift into a
handler failure.

## Prioritized Backlog

1. Accept Picasa entries only from a dictionary `feed` containing a list
   `entry` value.
2. Return the existing empty image list for missing or malformed feed
   containers.
3. Preserve valid entry ordering, per-entry filtering, response shape, network
   timeout, response-size, and top-level JSON guards.
4. Add focused characterization and hostile-mutation contracts plus repository
   guidance.
5. Keep Instagram pagination and map-provider nested schema validation as
   separate work.

## Implementation

- Add a small `picasa_entries` helper that normalizes malformed feed containers
  to an empty list.
- Route `PicasaHandler` through the helper before existing entry parsing.
- Extend characterization tests and the static baseline with helper-use and
  malformed-container contracts.
- Update README, SECURITY, VISION, CHANGES, and AGENTS guidance.

## Verification Plan

- Run focused integration tests, all characterization tests,
  `scripts/check-baseline.py`, `make lint`, `make test`, `make build`, and
  `make check`, Python 2 and Python 3 compilation, workflow parsing, whitespace
  checks, and intended-file secret/artifact scans.
- Remove the feed-type guard, remove the entry-list guard, and bypass the helper
  in the handler; each hostile mutation must fail.
- Take one bounded exact-head push, pull-request, and CodeQL snapshot after
  push; do not poll.

## Work Completed

- Pending implementation.

## Verification Completed

- Pending implementation and verification.
