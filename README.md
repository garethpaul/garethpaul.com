# garethpaul.com

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/garethpaul.com` is a static web project. GarethPaul.com Repo

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Python (14), JavaScript (2), shell (1).

## Repository Contents

- `CHANGES.md` - concise history of maintenance changes
- `Makefile` - local verification entry point
- `README.md` - project overview and local usage notes
- `main.py`
- `scripts/check-baseline.py` - static legacy runtime and integration checks
- `SECURITY.md` - security reporting and disclosure guidance
- `static` - source or example code
- `templates` - source or example code
- `tests/test_integration_guards.py` - pure-function characterization tests for
  legacy integration guardrails
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: static, templates
- Dependency and build manifests: none detected
- Entry points or build surfaces: main.py, app.yaml
- Test-looking files: scripts/check-baseline.py

## Getting Started

### Prerequisites

- Git
- Python 3 for static verification

### Setup

```bash
git clone https://github.com/garethpaul/garethpaul.com.git
cd garethpaul.com
```

The deployed app is a legacy Python 2 App Engine application. The private `const.py` file is intentionally not checked in; provide it only through local or platform-private configuration when reviving the app.

## Running or Using the Project

- App Engine routes are defined in `main.py` and configured by `app.yaml`.
- Private integration settings such as map, geocode, Instagram, Glass, and Picasa endpoints belong in local `const.py` or platform configuration, not git.

## Testing and Verification

Run the local static baseline and characterization checks:

```bash
make lint
make test
make build
make check
```

The `lint` and `build` targets delegate to `make check`. The `test` target runs
the dependency-free `tests/test_integration_guards.py` characterization tests.
The `check` target runs both `scripts/check-baseline.py` and the
characterization tests, verifies Python syntax, checks credential/cache
guardrails, and does not require App Engine or private credentials.

GitHub Actions runs the same `make check` gate through
`.github/workflows/check.yml` on pushes and pull requests.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- Detected references to Twitter, Google APIs, Instagram, Picasa, and Glass. Keep API keys, OAuth credentials, access tokens, private endpoints, and account-specific values in local configuration only.

## Security and Privacy Notes

- Review changes touching authentication or token handling; examples include `instagram.py`, `templates/stream.html`, and `base.py`.
- Review changes touching external API calls or credential-adjacent configuration; examples include `instagram.py`, `map.py`, `picasa.py`, `glass.py`, and `templates/profile.html`.
- Review changes touching network requests, sockets, or service endpoints; examples include `instagram.py`, `map.py`, `picasa.py`, and `glass.py`.
- Review changes touching JSON, template, or API-response parsing; examples include `base.py`, `glass.py`, `instagram.py`, `map.py`, and `picasa.py`.
- Instagram access tokens must not be placed in URL query strings. The checked-in proxy strips token query values from pagination URLs and sends the token through an authorization header.
- Instagram pagination URLs must remain on `https://api.instagram.com` before
  the proxy sends the bearer token header.
- Map API responses cache by request path/query and weather/geocode URLs are built with structured HTTPS query encoding.
- Private endpoints loaded from local `const.py`, including map location,
  Picasa, and Glass URLs, are validated as HTTPS URLs with hosts and no
  embedded credentials or fragments before the app fetches them.
- The template-facing Glass URL from `const.py` is also validated as an HTTPS
  URL with a host and no embedded credentials or fragments before the Stream
  page renders it into client-side image URLs.
- External template assets load through explicit HTTPS URLs so shared CSS,
  JavaScript, and analytics references do not inherit an insecure page scheme.
- Empty Picasa feed responses return an empty image list instead of raising
  while proxying legacy album data.
- Malformed Picasa album entries are skipped so one partial provider record does
  not break the whole image proxy response.

## Maintenance Notes

- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing
  changes to App Engine routing, API integrations, templates, or private
  configuration handling.
- See `docs/plans/2026-06-09-template-glass-url-validation.md` for the
  template-facing Glass URL guard.
- See `docs/plans/2026-06-09-private-endpoint-url-parts.md` for the private
  endpoint URL-parts guard.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for local verification
  target guardrails.
- See `docs/plans/2026-06-09-picasa-empty-feed-guard.md` for empty Picasa feed
  handling.
- See `docs/plans/2026-06-09-picasa-entry-shape-guard.md` for malformed Picasa
  album entry handling.
- See `docs/plans/2026-06-09-template-external-https.md` for explicit HTTPS
  template asset references.
- See `docs/plans/2026-06-10-ci-and-characterization-tests.md` for the CI and
  integration characterization baseline.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
