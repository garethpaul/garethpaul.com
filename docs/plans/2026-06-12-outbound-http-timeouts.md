# Outbound HTTP Timeout Boundary

status: completed

## Context

The legacy App Engine request handlers called `urllib2.urlopen` directly for
Instagram, Glass, Picasa, map-location, geocoding, and weather providers. Those
calls had no timeout, so a stalled provider could retain a request handler
indefinitely.

## Completed Scope

- Added one Python 2-compatible `open_url` helper with a 10-second timeout.
- Routed every checked-in outbound provider request through that helper.
- Preserved HTTPS endpoint validation and Instagram bearer-header behavior.
- Added dependency-free tests that prove the configured deadline reaches
  `urllib2.urlopen` and that request objects are passed through unchanged.
- Extended the static baseline so direct unbounded `urlopen` calls cannot return.

## Verification

- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `make check`
- mutations restoring a direct provider `urllib2.urlopen` call or removing the
  timeout argument must fail
- `git diff --check`

The timeout prevents indefinite waits; provider failures still use the legacy
handler error path. Adding retries or user-facing fallback payloads should be a
separate behavior-aware change to avoid multiplying traffic to failing services.
