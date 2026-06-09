# Changes

## 2026-06-08

- Added `make lint`, `make test`, and `make build` aliases so local verification
  has the expected pre-push gate targets in addition to `make check`.
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
