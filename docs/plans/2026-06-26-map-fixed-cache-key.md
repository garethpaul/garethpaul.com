# Map Fixed Cache Key

status: completed

## Goal

Make every `/api/map` request reuse the same bounded cache entry because query
parameters do not affect the generated map payload.

## Problem

`ApiHandler.get()` currently uses `self.request.path_qs` as the memcache key.
An arbitrary browser query therefore forces a miss, three private provider
requests, and a distinct long-lived cache entry even though `get_data()` never
reads request parameters. Google documents that legacy App Engine memcache is
global to the application, capacity is best effort, and keys are limited to
250 bytes. Query-controlled cache identity creates unnecessary pressure and
allows callers to bypass the existing cache cheaply.

## Design

1. Add executable hit and miss regressions with unrelated query strings.
2. Define one fixed, non-secret map cache key and the existing bounded TTL.
3. Use those constants for both cache reads and writes.
4. Document the fixed-key boundary in repository guidance.
5. Run focused tests, all Make gates, an external-root gate, and hostile
   mutations restoring query-derived cache identity.

## Non-Goals

- Changing map payload fields or provider endpoints.
- Changing the existing cache lifetime.
- Modernizing the Python 2 App Engine runtime.

## Evidence

- Google Cloud legacy memcache overview:
  https://docs.cloud.google.com/appengine/docs/legacy/standard/python/memcache

## Verification Completed

- The focused map cache hit and miss regressions and all 40 characterization
  tests passed.
- Every repository-root Make alias and the absolute external-directory
  `make check` gate passed without creating Python bytecode artifacts.
- In-memory compilation passed for `map.py`, the integration regressions, and
  the baseline checker; Python 2.7 was unavailable locally.
- Four isolated hostile mutations were rejected: query-derived identity,
  private-endpoint identity, an unbounded expiration, and removed security
  guidance.
- Implementation commit `781e51099e332a2730b145adb955ec9d339836cd`
  passed push Check run `28252751710`, pull-request Check run `28252753514`,
  and CodeQL run `28252753783` for Actions, Python, and JavaScript/TypeScript.
- Both hosted Check runs completed successfully for Python 3.10, 3.12, and
  3.14. No live provider request or credential was used.
