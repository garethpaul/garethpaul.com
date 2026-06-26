## GarethPaul.com Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

GarethPaul.com is the repository for a personal public website that moved from
Heroku to Google App Engine.

The repository is useful as a small App Engine-era personal site with templates,
static assets, profile/map/picture pages, and integration modules. Project
context lives in [`README.md`](README.md).

The goal is to keep the public site maintainable, lightweight, and safe around
personal data and external API integrations.

The current focus is:

Priority:

- Preserve the App Engine site structure and templates
- Keep public profile and page behavior easy to inspect
- Avoid committing private API credentials or personal data exports
- Keep `scripts/check-baseline.py`, `make lint`, `make test`, `make build`,
  `make check`, `tests/test_integration_guards.py`, and GitHub Actions passing
  for access-token query strings, Instagram pagination host checks, HTTPS API
  URLs, Picasa entry parsing, and cache-key guardrails
- Keep hosted characterization coverage green on Python 3.10, 3.12, and 3.14
- Offline verification uses one explicit, fail-fast Python 3 command while the
  deployment remains Python 2.
- Keep every canonical Make gate bytecode-free without caller configuration.
- Keep hosted checks pinned, read-only, credential-free, and non-deploying
- Keep every outbound provider request behind the shared 10-second deadline
- Refuse automatic provider redirects before validated URLs or bearer headers
  can be forwarded to another destination
- Keep provider payload reads behind the shared 1 MiB response limit
- Require standard or vendor application JSON media before provider JSON reads
- Require provider JSON to decode to top-level objects through one shared parser
- Render provider image values through HTTPS-only DOM property assignment
  instead of HTML string concatenation
- Keep security policy visible for the public site

Next priorities:

- Document local setup, deployment, and supported Python/App Engine runtime
- Review external integrations for current API compatibility
- Add simple route/template verification beyond the current static and
  pure-function characterization baseline
- Keep local verification targets available while the legacy App Engine runtime
  remains static-check only
- Modernize hosting/runtime in a dedicated pass if the site is revived

Contribution rules:

- One PR = one focused page, integration, deployment, or documentation change.
- Keep private credentials and generated data out of git.
- Verify affected routes locally before pushing.
- Preserve public-site simplicity over framework-heavy rewrites.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Personal websites can expose private API tokens, account data, or location/media
metadata. Future integration work should keep secrets in environment or platform
configuration and avoid publishing private data accidentally.

Current integration guardrails keep Instagram access tokens out of URL query
strings, require Instagram pagination host values to stay on
`https://api.instagram.com`, keep checked-in weather/geocode URL construction on
HTTPS, and verify the map API writes cache entries with a defined request key.
The Glass proxy should reuse successful validated provider objects for five
minutes under one fixed non-secret key so browser query strings cannot fragment
the cache and private endpoint values never become cache keys.
Malformed Instagram pagination objects and non-list media containers should
normalize safely before either provider page is combined.
Non-text Instagram pagination URL values should normalize to no next page while
preserving valid media from the current provider response.
The public webapp2 app keeps debug output disabled. Private integration endpoints
loaded through `settings.py` must also be HTTPS URLs with hosts and no embedded credentials or fragments before proxy handlers fetch them.
`settings.py` sources ignored local `const.py` values or documented
`GARETHPAUL_*` environment variables without committing secrets. The
template-facing Glass URL from `settings.py` must also be validated before
stream templates render it into client-side image URLs.
Empty Picasa feed responses should continue to return an empty image list
instead of raising while the legacy album integration remains available.
Malformed Picasa album entries should be skipped so partial provider records do
not break otherwise valid image proxy responses.
Picasa image source fields should normalize non-text values to no image while
preserving valid Unicode URL text.
The server-side Picasa URL policy should publish only HTTPS image URLs with a
host and no embedded credentials or fragment, independently of browser-side
image filtering.
Malformed Picasa feed objects and non-list entry containers should normalize to
the same empty image-list response before nested lookup or iteration.
External template assets should continue to use explicit HTTPS URLs for shared
CSS, JavaScript, and analytics references.
Provider image feeds should continue to use DOM property assignment and encode
Glass token values before constructing browser image URLs.
Outbound provider requests should continue to use the shared timeout instead of
calling `urllib2.urlopen` directly from handlers.
The shared opener should continue to reject automatic redirects rather than
forwarding provider requests or Instagram authorization headers.
Provider handlers should continue to use the shared bounded response reader
instead of calling `read()` directly.
Provider handlers should continue to reject malformed JSON and non-object
top-level values before accessing provider fields.

## What We Will Not Merge (For Now)

- Private credentials or personal data exports
- Broad framework migrations without a deployment plan
- Integrations that expose account data without clear purpose
- Generated assets unrelated to visible site behavior

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
