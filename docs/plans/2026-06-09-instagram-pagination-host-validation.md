# Instagram Pagination Host Validation

status: completed

## Context

The Instagram proxy strips `access_token` query values and sends the configured
token through an Authorization header. Pagination URLs come from provider JSON,
so they must be constrained before the proxy attaches bearer credentials to the
request.

## Completed Scope

- Added an Instagram API URL guard that requires HTTPS and the
  `api.instagram.com` host.
- Applied the guard after token-query stripping and before creating authorized
  `urllib2` requests.
- Extended the static baseline and docs so future changes preserve the
  credential boundary.

## Verification

- `make check`
- `git diff --check`
