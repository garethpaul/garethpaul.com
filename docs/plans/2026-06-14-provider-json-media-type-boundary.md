---
title: Provider JSON Media Type Boundary
date: 2026-06-14
status: completed
execution: code
---

## Context

Provider responses are bounded and top-level JSON shapes are validated, but
JSON-designated callers read and decode bodies without checking response media
metadata. A successful HTML or binary response can therefore consume the JSON
read/decode path instead of failing closed at the response boundary.

## Requirements

- Require `application/json` or an `application/*+json` media type before any
  JSON-designated provider response body is read.
- Close rejected responses without reading their bodies and keep error messages
  free of URLs, credentials, headers, and payloads.
- Preserve generic bounded `read_url` behavior for non-JSON callers and retain
  the shared timeout, redirect rejection, byte limit, and object-shape checks.
- Route shared JSON-object and Instagram JSON requests through the opt-in media
  boundary.
- Add focused executable tests, mutation-sensitive static contracts,
  synchronized guidance, and truthful completed verification evidence.

## Non-Goals

- Changing provider endpoints, credentials, pagination, cache keys, response
  schemas, or dependency versions.
- Accepting `text/json`, `text/javascript`, or missing/malformed media types.
- Claiming credentialed App Engine or live provider validation.

## Verification Plan

- Start with focused media-type and unread-body regressions, then run the full
  dependency-free suite and all Make gates from repository and external
  directories.
- Reject mutations that remove media validation, widen the allowlist, read
  before validation, bypass an opt-in caller, remove executable coverage, or
  falsify completed plan evidence.
- Compile production modules with Python 3 and Python 2 when available; audit
  the exact diff, generated artifacts, workflows/dependencies, whitespace,
  conflict markers, and changed-line credential patterns.
- Take one bounded exact-head pull-request and security-alert snapshot without
  polling.

## Work Completed

- Added a shared response-media helper that accepts standard and vendor
  application JSON types across Python 2 and Python 3 response-header APIs.
- Added an opt-in JSON boundary to the existing bounded reader and required the
  shared JSON-object and Instagram request paths to use it before body reads.
- Added focused unread-body and compatibility regressions, a mutation-sensitive
  checker, baseline integration, and synchronized repository guidance.

## Verification Completed

- The focused provider media tests passed for standard/vendor JSON acceptance,
  missing/text/binary rejection before reads, generic-read compatibility, and
  both JSON caller opt-ins.
- The complete dependency-free suite passed all 25 tests.
- Python 3 and Python 2 production-module compilation passed.
- All four Make gates and the external-directory Make gate passed.
- The seven hostile mutations were rejected across validator removal,
  allowlist widening, read ordering, both caller bypasses, executable coverage,
  and completed-plan evidence.
- Exact diff, generated-artifact, executable-mode, workflow/dependency,
  whitespace, conflict-marker, and changed-line credential audits passed.
- No credentialed App Engine request or live provider call was performed.
- The hosted pull-request and security-alert result is recorded against the
  exact pushed head in the external engineering tracker.
