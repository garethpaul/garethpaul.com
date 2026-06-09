# Private Endpoint URL Parts

status: completed

## Context

`const.py` is intentionally private, but its endpoint values feed handlers and
templates directly. The current shared URL validator requires HTTPS and a host;
it should also reject embedded URL credentials and fragments so private endpoint
configuration cannot carry confusing or sensitive URL parts.

## Objectives

- Reject private endpoint URLs with usernames, passwords, or fragments.
- Keep the existing HTTPS and host checks for `map_api`, `picasa_api`,
  `glass_api`, and the template-facing Glass URL.
- Extend the static baseline and docs so the URL-parts boundary remains visible.

## Verification

- `scripts/check-baseline.py`
- `make check`
- `git diff --check`
