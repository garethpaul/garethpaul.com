# AGENTS.md

## Repository purpose

`garethpaul/garethpaul.com` is a static web project. GarethPaul.com Repo

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `templates` - server-rendered templates

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Offline verification uses one explicit, fail-fast Python 3 command while the
  deployment remains Python 2. Override it with
  `make PYTHON=/path/to/python3 check` when needed.
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Python (14), JavaScript (2), shell (1).
- Prefer dependency-free tests or stdlib checks when legacy packages are unavailable.

## Testing guidance

- `tests/test_integration_guards.py` and `tests/test_template_image_rendering.py` provide dependency-free characterization coverage; `make check` is the maintained full gate.
- Canonical Make gates must disable Python bytecode writes so verification does
  not create repository-local cache artifacts.
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Twitter, Google APIs, Instagram, Picasa, and Glass. Keep API keys, OAuth credentials, access tokens, private endpoints, and account-specific values in local configuration only.
- `settings.py` may load private values from ignored local `const.py` or
  documented `GARETHPAUL_*` environment variables; do not commit real values.
- Instagram access tokens must not be placed in URL query strings. The checked-in proxy strips token query values from pagination URLs and sends the token through an authorization header.
- Instagram pagination URLs must remain on `https://api.instagram.com` before the proxy sends the bearer token header.
- Normalize malformed Instagram pagination and media containers before
  following or combining provider pages.
- Non-text Instagram pagination URL values must normalize to no next page
  before the proxy attempts URL parsing.
- Map API responses cache by request path/query and weather/geocode URLs are built with structured HTTPS query encoding.
- Glass API responses cache only successful validated objects for five minutes
  under a fixed non-secret key; do not key this cache by browser queries or the
  configured private endpoint.
- Private endpoints loaded through `settings.py`, including map location, Picasa, and Glass URLs, are validated as HTTPS URLs with hosts and no embedded credentials or fragments before the app fetches them.
- Normalize malformed Picasa feed objects and non-list entry containers before
  nested lookup or iteration; preserve the empty image-list fallback.
- Non-text Picasa image source values must normalize to no image before handler
  output; preserve valid Python 2/3 text values, including Unicode URLs.
- Picasa image source URLs must pass `base.require_https_url` before handler
  output; keep this server policy separate from the browser's HTTPS filter.
- The template-facing Glass URL from `settings.py` is also validated as an HTTPS URL with a host and no embedded credentials or fragments before the Stream page renders it into client-side image URLs.
- All outbound provider calls must use `base.open_url` so the shared 10-second timeout remains enforced; do not add direct handler-level `urllib2.urlopen` calls.
- The shared provider opener must refuse automatic redirects so private
  requests and Instagram bearer headers are not forwarded to unvalidated URLs.
- JSON-designated provider reads must require `application/json` or an
  `application/*+json` media type before reading and close rejected responses
  without consuming their bodies.
- Keep `.github/workflows/check.yml` aligned with the exact baseline contract: immutable action pins, read-only permissions, no persisted checkout credentials, no deployment steps, and the documented Python matrix.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
