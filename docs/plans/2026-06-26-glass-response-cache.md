---
title: Glass Response Cache
date: 2026-06-26
status: completed
execution: code
---

## Context

The Glass API handler validates and fetches the same private JSON endpoint on
every browser request even though the repository already provides an App
Engine memcache helper. The source has carried an explicit TODO to limit these
upstream requests since the handler was introduced.

## Decision

- Cache only successfully validated top-level JSON objects.
- Use one fixed, non-secret cache key because browser query strings do not
  affect the upstream request and the configured endpoint may contain private
  values.
- Expire entries after five minutes so provider updates remain bounded in age.
- Preserve the existing HTTPS, timeout, redirect, media-type, response-size,
  and object-shape boundaries on cache misses.
- Preserve the current handler response shape and error behavior.

## Non-Goals

- Caching provider errors or invalid payloads.
- Changing the private Glass endpoint, response schema, or browser refresh
  behavior.
- Modernizing the legacy App Engine runtime or the existing map cache.

## Implementation Plan

1. Add dependency-free cache-hit and cache-miss behavior tests.
2. Add a fixed-key, bounded cache path for successful Glass objects.
3. Route the handler through that path and remove the completed TODO.
4. Add baseline and project-guidance contracts.
5. Run focused tests, all Make gates, mutations, and exact-diff audits.

## Verification Plan

- Prove a cache hit returns without calling the provider reader.
- Prove a cache miss writes the validated object with the fixed key and
  five-minute expiration.
- Run the maintained test suite and all canonical Make aliases from repository
  and external working directories.
- Reject mutations that bypass the cache, derive the key from request or
  endpoint data, remove expiry, remove behavior coverage, or falsify plan
  completion.

## Verification Completed

- All three focused Glass cache tests passed for hit short-circuiting,
  successful bounded miss writes, and failure non-caching.
- All 38 dependency-free tests, the baseline checker, all four canonical Make
  aliases, and the external-directory Make gate passed.
- Six isolated mutations were rejected across cache reads, secret-derived
  keys, expiry, handler routing, failure coverage, and plan completion.
- No private configuration, App Engine credential, or live provider request
  was used.
