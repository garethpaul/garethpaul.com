# Provider JSON Object Shape Boundary

status: in_progress

## Context

The Instagram, Glass, Picasa, map-location, geocoding, and weather integrations
all expect provider JSON to decode to an object. They currently call
`json.loads` independently and then assume dictionary methods or keys exist.
A valid JSON array, string, number, boolean, or null therefore fails later with
an incidental type or index error instead of at one documented provider
boundary. The map-location path also decodes the same response twice.

## Scope

1. Add one Python 2-compatible helper that decodes a bounded provider response
   and rejects non-object top-level JSON values.
2. Route every provider JSON decode through the shared helper without changing
   successful response payloads, cache behavior, endpoint validation, timeout,
   or response-size limits.
3. Add dependency-free characterization for accepted objects, malformed JSON,
   and every valid non-object JSON type.
4. Extend the static baseline and mutation suite so direct provider
   `json.loads` calls and removal of the object guard fail.
5. Update README, SECURITY, VISION, and CHANGES with the boundary.

## Verification Plan

- Run focused and full unittest discovery, `scripts/check-baseline.py`, all four
  Make gates, Python 3 compilation, Python 2 production-module compilation when
  available, workflow parsing, diff checks, and intended-file secret scans.
- Mutate away the object type check, restore a direct provider `json.loads`, and
  remove non-object characterization coverage; each mutation must fail.
- Push a stacked pull request and take one bounded exact-head workflow, check,
  and CodeQL snapshot without polling.

## Risk And Rollback

The helper intentionally changes only malformed or unexpected provider
responses. A rollback removes the helper and restores the existing direct
decodes; no data migration, cache format change, credential change, or deploy
operation is involved.
