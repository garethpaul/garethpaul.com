# Private Endpoint Host Validation

status: completed

## Context

The checked-in map, Picasa, and Glass proxy handlers already require private
endpoint settings to use HTTPS. Hostless HTTPS strings are still malformed for
network fetches and should fail closed before `urllib2.urlopen` sees them.

## Completed Scope

- Updated `require_https_url` to parse endpoint settings once and require both
  the `https` scheme and a non-empty host.
- Extended the static baseline to preserve the host requirement.
- Updated README, VISION, and CHANGES with the stricter private endpoint
  contract.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
