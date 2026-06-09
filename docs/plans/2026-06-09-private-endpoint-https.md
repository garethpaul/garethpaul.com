# Private Endpoint HTTPS Guard

status: completed

## Context

The repository intentionally omits private `const.py` values, but the checked-in
proxy handlers still decide how those values are used. The map, Picasa, and
Glass integrations should fail closed if a private endpoint is accidentally
configured with plain HTTP.

## Completed Scope

- Added a shared `require_https_url` helper for private endpoint values.
- Applied the helper before opening map, Picasa, and Glass private API URLs.
- Extended the static baseline and docs so private endpoint fetches remain
  HTTPS-only.

## Verification

- `make check`
- `git diff --check`

## Follow-Ups

- Replace legacy private `const.py` usage with platform environment variables
  when the App Engine runtime is modernized.
