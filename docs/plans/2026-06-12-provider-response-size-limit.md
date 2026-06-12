# Provider Response Size Limit

status: planned

## Context

All outbound Instagram, Glass, Picasa, map-location, geocoding, and weather
requests now use a shared 10-second timeout. Each handler still calls
`response.read()` without a size, so a provider can return a fast but
unexpectedly large payload that is fully buffered before JSON decoding.

The proxied responses are small metadata documents. They do not need an
unbounded memory budget in the legacy App Engine request process.

## Priority

The timeout bounds elapsed provider work but not response memory. A shared read
limit completes that availability boundary and gives every provider the same
failure behavior.

## Prioritized Backlog

1. Limit provider response bodies to 1 MiB plus one detection byte.
2. Accept payloads exactly at the limit and reject larger payloads before JSON
   decoding or cache writes.
3. Close provider responses after bounded reads on both success and failure.
4. Route every checked-in provider payload through the shared helper.
5. Extend characterization tests, the static baseline, and maintenance docs.

## Implementation

- Add `MAX_PROVIDER_RESPONSE_BYTES` and `read_url` to `base.py` using Python
  2-compatible `read(size)` and `close()` calls.
- Raise `ValueError` when the extra detection byte is present.
- Keep `open_url` as the tested request/deadline boundary and build `read_url`
  on top of it.
- Replace direct provider `open_url(...).read()` calls with `read_url(...)`.
- Test exact-boundary, oversized, close-on-success, and close-on-error behavior
  with dependency-free fakes.

## Verification

- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `python3 scripts/check-baseline.py`
- `make check`
- `make lint`
- `make test`
- `make build`
- `python3 -m compileall -q .`
- `git diff --check`
- Mutations removing the extra-byte read, oversized rejection, response close,
  or a provider's `read_url` routing must fail.

Live provider and App Engine deployment tests remain out of scope because the
private configuration and unsupported Python 2 runtime are unavailable here.
