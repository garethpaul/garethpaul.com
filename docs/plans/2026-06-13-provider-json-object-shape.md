# Provider JSON Object Shape Boundary

status: completed

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

## Work Completed

- Added shared bounded-read and decode helpers with one top-level object guard.
- Routed Instagram, Glass, Picasa, map-location, geocoding, and weather parsing
  through the shared decoder while preserving successful payload behavior.
- Added accepted-object, malformed-JSON, and all non-object JSON type coverage.
- Extended the static baseline and synchronized repository documentation.

## Verification Completed

- The 14 focused integration characterization tests passed.
- All four Make gates and all 16 characterization tests passed.
- Python 3 and Python 2 compilation passed for the production modules; Python 3
  also compiled the tests and checker.
- The non-object JSON mutation failed with `ValueError not raised` assertions.
- The direct provider `json.loads` mutation failed with the shared-decoder
  baseline error.
- The removed non-object test-contract mutation failed with the expected
  characterization coverage error.
- Plan status and completed-evidence mutations failed with the plan verification
  contract error.
- The hosted pull-request and CodeQL snapshot is recorded separately after push;
  this plan claims only the completed pre-push verification above.
