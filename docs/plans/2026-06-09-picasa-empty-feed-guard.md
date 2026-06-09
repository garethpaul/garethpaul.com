# Picasa Empty Feed Guard

status: completed

## Context

`picasa.py` expects the legacy provider payload to include `feed.entry`.
If the album is empty or the provider returns a partial response, the proxy can
raise a `KeyError` instead of returning an empty image list to the site.

## Completed Scope

- Read Picasa entries through nested defaults so missing feed data becomes an
  empty list.
- Kept the response shape stable as `{"data": []}` when no images are present.
- Extended the static baseline and docs so the empty-feed behavior remains
  visible.

## Verification

- `scripts/check-baseline.py`
- `make check`
- `git diff --check`
