---
title: Provider Redirect Boundary
date: 2026-06-14
status: planned
execution: code
---

## Context

Provider URLs and Instagram pagination URLs are validated before requests are
issued, but Python 2.7 `urllib2` follows HTTP redirects automatically. Its
standard redirect handler copies request headers other than content metadata,
so an Instagram bearer `Authorization` header can be forwarded to a redirected
host before application-level URL validation runs.

## Priority

1. Prevent bearer credentials and private provider requests from crossing an
   unvalidated HTTP redirect boundary.
2. Preserve the shared timeout, bounded response read, response cleanup, and
   existing provider URL validation contracts.
3. Keep the legacy Python 2 App Engine runtime and dependency-free Python 3
   characterization environment working.

## Requirements

- Add one shared `urllib2` opener whose redirect handler refuses automatic
  redirects.
- Route every provider request through that opener with the existing ten-second
  timeout.
- Keep Instagram bearer credentials only on the original validated
  `api.instagram.com` request.
- Add characterization tests for redirect refusal, opener reuse, request-object
  identity, and timeout propagation.
- Extend the static checker, synchronized guidance, and completed-plan evidence
  so redirect handling cannot silently regress.

## Non-Goals

- Following same-host redirects or introducing a redirect allowlist.
- Changing provider endpoints, credentials, response parsing, payload limits,
  caching, templates, dependencies, or App Engine deployment metadata.
- Claiming credentialed live-provider behavior.

## Implementation Units

### Shared Transport Boundary

Files: `base.py`

- Define a Python 2-compatible redirect handler that refuses redirect request
  creation, construct one module-level opener, and use it from `open_url`.

### Characterization And Static Contracts

Files: `tests/test_integration_guards.py`, `scripts/check-baseline.py`

- Model the opener/handler APIs in the Python 3 compatibility stubs and prove
  redirect refusal, shared-opener usage, timeout propagation, and bearer request
  preservation.
- Require the implementation, tests, guidance, and truthful plan evidence.

### Guidance

Files: `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`, `AGENTS.md`

- Document fail-closed provider redirects and the continuing lack of live
  credentialed validation.

## Verification Plan

- Run focused and complete characterization tests, the direct baseline, all
  four Make gates, Python 2 production-module compilation, Python 3 validation
  compilation, and the external-directory Make gate.
- Reject isolated mutations that restore `urllib2.urlopen`, allow redirect
  request creation, construct per-request openers, drop timeout propagation,
  weaken focused tests, or falsify completed plan evidence.
- Audit exact changed paths, generated artifacts, whitespace, conflict markers,
  executable modes, and credential-like additions before commit and push.
- Take one bounded exact-head pull-request and code-scanning snapshot without a
  poll or watch loop.

## Work Completed

- Not yet implemented.

## Verification Completed

- Not yet run.
