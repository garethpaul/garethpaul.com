# Changes

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
