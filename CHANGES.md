# Changes

## 2026-06-08

- Added an HTTPS-only guard for private map, Picasa, and Glass endpoint values
  loaded from local `const.py`.
- Removed Instagram access-token query string construction and now send the token via an authorization header.
- Switched checked-in weather/geocode URL construction to structured HTTPS requests.
- Fixed the map API cache write to use a defined request cache key.
- Handled empty geocoding responses without raising an index error.
- Disabled public webapp2 debug output.
- Added `make check` and static baseline checks that run without private App Engine credentials.
