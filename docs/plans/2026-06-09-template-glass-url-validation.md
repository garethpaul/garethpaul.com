# Template Glass URL Validation

status: completed

## Context

The Glass stream template builds client-side image URLs from `const.glass_url`.
Private proxy endpoints already require HTTPS URLs with hosts before server-side
fetches, but the template-facing Glass URL also needs the same validation before
rendering into HTML.

## Completed Scope

- Validated `const.glass_url` with `require_https_url` before passing it to
  templates.
- Extended the static baseline to preserve the template-facing Glass URL guard.
- Kept README, VISION, and CHANGES aligned with the validation contract.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
