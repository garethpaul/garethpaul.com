---
title: "fix: Validate Picasa image URLs"
type: fix
date: 2026-06-17
status: completed
---

# fix: Validate Picasa image URLs

## Summary

Filter Picasa image sources through the repository's established private URL
policy before publishing them from `/api/picasa`, so API clients receive only
HTTPS URLs with a host and no embedded credentials or fragment.

## Problem Frame

The latest Picasa source-shape guard accepts only Python 2/3 text values, but
all text is still published. Values such as `http:` URLs, `data:` URLs,
credential-bearing URLs, fragments, and arbitrary strings therefore remain in
the JSON API even though the current browser helper independently refuses
non-HTTPS sources. The server contract should fail closed for every client.

## Requirements

- R1. Picasa image sources must use HTTPS and include a host before publication.
- R2. Sources with embedded usernames, passwords, or fragments must be ignored.
- R3. Valid HTTPS sources must preserve paths, query strings, ports, and Unicode
  text exactly as provided.
- R4. Non-text source values must continue to be rejected before URL parsing.
- R5. Maintained checks and project guidance must preserve the URL policy and
  distinguish it from the existing client-side image filter.

## Key Technical Decisions

- KTD1. Reuse `base.require_https_url` as the single URL policy rather than
  introducing a Picasa-specific parser with divergent rules.
- KTD2. Convert URL-policy `ValueError` failures to `None` in
  `picasa_entry_src`; one malformed provider entry must not fail the whole feed.
- KTD3. Keep source-shape validation before URL validation so Python 2/3 text
  compatibility remains explicit and non-text values never reach `urlsplit`.
- KTD4. Preserve the current client-side HTTPS image helper as a separate
  defense; this change strengthens the API response rather than removing the
  browser boundary.

## Implementation Units

### U1. Enforce the Picasa image URL policy

- **Goal:** Publish only sources accepted by the shared HTTPS URL validator.
- **Files:** `picasa.py`, `tests/test_integration_guards.py`
- **Patterns:** Follow `require_https_url` behavior while retaining
  `picasa_entry_src`'s fail-closed `None` result.
- **Test scenarios:** Accept HTTPS URLs with queries and Unicode paths; reject
  HTTP, data, hostless, credential-bearing, fragment-bearing, arbitrary text,
  and existing non-text values; continue processing valid sibling entries.
- **Verification:** Focused Picasa tests and the complete compatibility suite
  pass under the maintained Python gate.

### U2. Make the boundary durable

- **Goal:** Extend static, mutation, security, and contributor contracts for
  server-side Picasa URL filtering.
- **Files:** `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
  `AGENTS.md`, `CHANGES.md`,
  `docs/plans/2026-06-17-002-fix-picasa-image-url-boundary-plan.md`
- **Patterns:** Require the shared validator call, failure conversion, ordering,
  focused regressions, and explicit server/client defense distinction.
- **Test scenarios:** Removing validation, accepting HTTP, moving URL parsing
  before the text guard, removing hostile URL coverage, or weakening plan
  evidence must fail the maintained gate.
- **Verification:** Root and external-directory checks pass, plus isolated
  hostile mutations for each contract dimension.

## Scope Boundaries

- No changes to Picasa endpoint configuration, provider fetching, response size,
  redirects, media-type validation, or top-level/container shape handling.
- No host allowlist is introduced because retired Picasa deployments may use
  different Google-hosted image domains.
- No browser helper or template behavior is removed or relaxed.
- No live Picasa/Google feed or App Engine deployment is exercised.
- PR stacking remains based on the terminal Picasa source-shape branch; no
  existing PR is merged or closed.

## Risks

- Previously published non-HTTPS or malformed source strings will disappear
  from the API response, which is the intended fail-closed behavior.
- The shared policy permits explicit ports and query strings; changing those
  semantics would affect private endpoint configuration and is outside scope.

## Verification Completed

- The 8 focused Picasa tests and all 30 characterization tests passed, so the
  focused and all characterization tests passed without provider credentials.
- All four Make gates passed: `make lint`, `make test`, `make build`, and
  `make check` exercised the maintained baseline from the repository root.
- The repository-root and external-directory `make check` passed, preserving
  the location-independent verification contract.
- Python 2.7 `picasa.py` compilation passed alongside Python 3 compilation of
  the changed runtime, test, and checker modules.
- Five isolated hostile mutations were rejected: removing or bypassing the
  shared validator, moving URL validation before the text guard, deleting the
  hostile-URL regression contract, and weakening this evidence record.
- No live Picasa request was executed; validation used dependency-free fixtures
  and static contracts only.
