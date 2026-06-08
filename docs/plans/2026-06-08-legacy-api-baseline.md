# GarethPaul.com Legacy API Baseline Plan

status: completed

## Context

`garethpaul.com` is a legacy Python 2 Google App Engine personal site. The repository intentionally omits private `const.py` credentials, so local verification needs to rely on syntax and static guardrails unless a maintainer supplies the old App Engine runtime and private configuration.

## Objectives

- Stop building Instagram API URLs that include the access token in the query string.
- Keep location and weather API requests on HTTPS where the checked-in code controls the endpoint.
- Fix the map API cache setter so it uses a defined request key.
- Handle empty geocoding responses without raising an index error.
- Disable public webapp2 debug output.
- Add a reproducible local `make check` baseline that does not require App Engine or private credentials.
- Document the current runtime and credential expectations.

## Work Items

1. Added `Makefile` and `scripts/check-baseline.py`.
2. Moved Instagram requests to Authorization headers and stripped token query values from pagination URLs.
3. Kept checked-in map/weather requests on HTTPS with URL-encoded query parameters.
4. Fixed the map cache setter to use `cache_key`.
5. Handled empty geocoding responses with an empty-address fallback.
6. Disabled webapp2 debug output on the WSGI app.
7. Updated README, VISION, SECURITY, CHANGES, and the recorded bug resolution.

## Verification

- `make check`
- `python3 -m py_compile *.py scripts/check-baseline.py`
- `git diff --check`
