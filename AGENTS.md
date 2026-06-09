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
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Python (14), JavaScript (2), shell (1).
- Prefer dependency-free tests or stdlib checks when legacy packages are unavailable.

## Testing guidance

- No dedicated test files were detected; treat `make check` as the minimum baseline.
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Twitter, Google APIs, Instagram, Picasa, and Glass. Keep API keys, OAuth credentials, access tokens, private endpoints, and account-specific values in local configuration only.
- Instagram access tokens must not be placed in URL query strings. The checked-in proxy strips token query values from pagination URLs and sends the token through an authorization header.
- Instagram pagination URLs must remain on `https://api.instagram.com` before the proxy sends the bearer token header.
- Map API responses cache by request path/query and weather/geocode URLs are built with structured HTTPS query encoding.
- Private endpoints loaded from local `const.py`, including map location, Picasa, and Glass URLs, are validated as HTTPS URLs with hosts and no embedded credentials or fragments before the app fetches them.
- The template-facing Glass URL from `const.py` is also validated as an HTTPS URL with a host and no embedded credentials or fragments before the Stream page renders it into client-side image URLs.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
