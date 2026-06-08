# Issue 4 Urlopen Timeouts

## Issue

`garethpaul/garethpaul.com#4` reports several `urllib2.urlopen(...).read()`
calls without explicit timeouts.

## Plan

- Add a shared `http_client.read_url` helper with a bounded timeout.
- Replace direct outbound `urllib2.urlopen` reads in map, Instagram, Glass, and
  Picasa handlers.
- Raise clear runtime errors for socket timeouts and URL errors.
- Add fake-urllib2 tests for timeout argument and error wrapping.
- Add a source baseline check to prevent direct timeout-less urlopen calls.

## Verification

- `python3 http_client_tests.py`
- `python3 -m py_compile http_client.py http_client_tests.py`
- `scripts/check-baseline.sh`
- `git diff --check`
