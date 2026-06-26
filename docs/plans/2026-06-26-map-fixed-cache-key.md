# Map Fixed Cache Key

status: active

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
