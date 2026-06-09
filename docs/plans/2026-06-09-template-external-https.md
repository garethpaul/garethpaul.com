# Template External HTTPS

status: completed

## Context

`templates/base.html` loads shared CSS, JavaScript, and analytics assets in the
browser. Protocol-relative URLs inherit the current page scheme, so an HTTP
request can make those third-party assets load over HTTP as well.

## Completed Scope

- Replaced protocol-relative CDN and analytics references with explicit HTTPS
  URLs.
- Extended `scripts/check-baseline.py` so the base template cannot reintroduce
  protocol-relative external browser asset URLs.
- Documented the guard in README, VISION, SECURITY, and CHANGES.

## Verification

- `scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
