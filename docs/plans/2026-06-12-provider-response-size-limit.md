# Provider Response Size Limit

status: completed

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

## Work Completed

- Added a shared 1 MiB provider response limit with one extra detection byte,
  exact-boundary acceptance, oversized-response rejection, and deterministic
  response cleanup.
- Routed every checked-in Instagram, Glass, Picasa, map-location, geocoding,
  and weather payload through the bounded helper before decoding or caching.
- Added characterization and static contracts for the size boundary, cleanup,
  and provider routing behavior.

## Verification Completed

- All four Make gates, 13 characterization tests, Python compilation, and
  `git diff --check` passed locally.
- Implementation push run `27393292065` and pull-request run `27393296845`
  passed at commit `cbd76a513ac8a075f9757bd60d7e62886bd3a517` across Python
  3.10, 3.12, and 3.14.
- Post-merge push run `27393311075` and CodeQL run `27402321576` passed at
  default-branch merge commit `837ee90fbd7998945133512348ca773342864b6a`.
- Mutations removing the extra-byte read, oversized rejection, response close,
  or any provider's bounded-helper routing were rejected by the baseline.
