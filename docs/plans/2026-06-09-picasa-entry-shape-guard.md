# Picasa Entry Shape Guard

status: completed

## Context

The Picasa proxy already treats missing or empty `feed.entry` data as an empty
image list. A partial provider entry inside an otherwise valid feed can still
omit `content.src`, which raises while building the image response.

## Completed Scope

- Added a small Picasa entry parser that only returns image sources from entries
  with the expected dictionary shape.
- Skipped malformed or incomplete entries while preserving the existing
  `{"data": [...]}` response shape for valid image URLs.
- Extended the static baseline and docs so the malformed-entry behavior remains
  visible.

## Verification

- `scripts/check-baseline.py`
- `make check`
- `git diff --check`
