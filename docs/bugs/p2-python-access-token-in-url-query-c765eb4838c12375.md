# [P2] Send API access tokens outside URL query strings

## Severity

P2 - security/credential-exposure

## Evidence

- `instagram.py:8`: `instagram_url = "https://api.instagram.com/v1/users/" + str(const.instagram_id) + "/media/recent?access_token=" + const.instagram_access_token`
- `instagram.py:13`: `result = urllib2.urlopen(instagram_url).read()`

## Problem

The code builds API request URLs with `access_token` in the query string. Query strings are commonly captured by server logs, proxy logs, analytics, crash reports, and referrer headers, so bearer-style tokens can leak outside the process that needs them.

## Suggested fix

Pass tokens in an `Authorization` header or the provider SDK's credential field when supported. If the provider requires query parameters, keep the token scoped and short-lived, redact URLs before logging, and avoid storing the full tokenized URL in module-level constants.

## Review metadata

- Repository: `garethpaul/garethpaul.com`
- Reviewed commit: `13ff99df3495fba6fc26680a6ebcead03d8f411e`
- Labels: `bug`, `codex-review`, `severity:P2`
- Codex review fingerprint: `c765eb4838c12375`
