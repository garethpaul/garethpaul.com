# Changes

## 2026-06-26 09:56:39 PDT

- Priority: security / upstream request amplification.
- Replaced query-derived map cache entries with one fixed non-secret key,
  preventing arbitrary browser queries from bypassing the cache and repeating
  three private provider requests.
- Preserved the existing 8,000-second expiration and map response payload.
- Files: `map.py`, `tests/test_integration_guards.py`,
  `scripts/check-baseline.py`,
  `docs/plans/2026-06-26-map-fixed-cache-key.md`, and synchronized repository
  guidance.
- Tests: focused cache hit/miss regressions, all 40 characterization tests,
  every root Make alias, the absolute external Make gate, in-memory syntax
  compilation, and four isolated hostile mutations pass locally.
- Findings: no open pull requests or issues overlap this change; only stale
  June 8-9 remote branches remain.
- Blockers: Python 2.7 is unavailable locally; the hosted Python matrix is the
  authoritative cross-runtime evidence. Codex review authentication may be
  unavailable and will be skipped after one HTTP 401 attempt.
- Next action: push the implementation, record exact hosted matrix and CodeQL
  evidence, then merge only that verified head.

## 2026-06-26

- Cached successful Glass API objects under a fixed non-secret key for five
  minutes, avoiding one private upstream request per browser refresh.

## 2026-06-18

- Made every canonical Make gate disable repository Python bytecode writes by
  default and added an isolated full-gate regression.
- Kept maintained Python syntax validation in memory so bytecode-disabled
  checks do not repopulate repository cache artifacts.

## 2026-06-17

- Filtered Picasa image sources through the shared HTTPS URL policy before API
  publication while retaining the browser's independent HTTPS image filter.
- Normalized non-text Picasa image source values to no image while preserving
  valid Unicode URL strings.

## 2026-06-16

- Ignored non-text Instagram pagination URL values while preserving valid media
  from the current provider response.
- Offline verification uses one explicit, fail-fast Python 3 command while the
  deployment remains Python 2.

## 2026-06-14

- Required JSON-designated provider responses to declare a standard or vendor
  application JSON media type before bounded body reads.
- Rejected automatic provider redirects through one shared opener so validated
  requests and Instagram bearer headers cannot be forwarded to another host.

## 2026-06-13

- Made legacy API verification independent of the caller's working directory
  by rooting checker and unittest execution in the loaded Makefile.
- Normalized malformed Instagram pagination and media containers on both pages
  before following pagination or combining provider values.
- Normalized malformed Picasa feed objects and non-list entry containers to the
  existing empty image-list response before iteration.
- Required all provider JSON responses to decode to top-level objects through a
  shared parser before handlers access provider fields.

## 2026-06-12

- Limited provider response bodies to 1 MiB, closed responses after bounded
  reads, and rejected oversized payloads before JSON decoding or cache writes.
- Added one bounded outbound HTTP helper and routed Instagram, Glass, Picasa,
  map-location, geocoding, and weather requests through its 10-second timeout.
- Added dependency-free regression coverage for timeout propagation while
  preserving Instagram bearer-header request behavior.
- Disabled checkout credential persistence and made the pinned Python matrix an
  exact baseline contract that rejects duplicate or weakened workflow keys.

## 2026-06-10

- Replaced provider-controlled image HTML concatenation with an HTTPS-only DOM
  helper and encoded Glass token values before browser URL construction.
- Added a pinned, least-privilege Python 3.10/3.12/3.14 GitHub Actions matrix
  that runs `make check`.
- Added characterization tests for private endpoint URL validation, Instagram
  bearer-token pagination requests, and malformed Picasa entry handling.
- Updated `make test` and `make check` so local gates run the behavior
  characterization coverage without App Engine credentials.

## 2026-06-09

- Skipped malformed Picasa album entries instead of raising when a partial
  provider record lacks `content.src`.

## 2026-06-08

- Replaced protocol-relative template asset URLs with explicit HTTPS
  references for shared CSS, JavaScript, and analytics assets.
- Added `make lint`, `make test`, and `make build` aliases so local verification
  has the expected pre-push gate targets in addition to `make check`.
- Returned an empty image list for empty Picasa feed responses instead of
  raising while proxying album data.
- Added an HTTPS-only guard for private map, Picasa, and Glass endpoint values
  loaded from local `const.py`.
- Added `settings.py` so clean checkouts can load private configuration from
  ignored `const.py` or documented `GARETHPAUL_*` environment variables with a
  clear setup error.
- Required those private endpoint URLs to include a host before fetching.
- Rejected embedded credentials or fragments in private endpoint URLs before
  handlers or templates use them.
- Required Instagram pagination URLs to stay on `https://api.instagram.com`
  before sending bearer credentials.
- Validated the template-facing Glass URL before rendering it into stream image
  URLs.
- Removed Instagram access-token query string construction and now send the token via an authorization header.
- Switched checked-in weather/geocode URL construction to structured HTTPS requests.
- Fixed the map API cache write to use a defined request cache key.
- Handled empty geocoding responses without raising an index error.
- Disabled public webapp2 debug output.
- Added `make check` and static baseline checks that run without private App Engine credentials.
