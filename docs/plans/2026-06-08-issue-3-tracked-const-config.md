---
title: Issue 3 Tracked Const Config
type: fix
status: active
date: 2026-06-08
origin: https://github.com/garethpaul/garethpaul.com/issues/3
execution: code
---

# Issue 3 Tracked Const Config

## Summary

Add a tracked, secret-free `const.py` configuration module so clean checkouts can import the application without a missing local file.

## Problem Frame

Issue #3 was filed from the public repository review because several modules import `const`, but the repository does not include `const.py`, a `const` package, or an example/template. A clean checkout fails before runtime behavior can be exercised.

## Requirements

- R1. The repository must include a tracked `const.py` module.
- R2. The module must expose every name currently referenced by application code: `map_api_key`, `geocode_key`, `instagram_id`, `instagram_access_token`, `glass_url`, `glass_api`, `picasa_api`, and `map_api`.
- R3. The module must not commit private API keys, tokens, or personal feed URLs.
- R4. Configuration should be documented for local and deployed environments.
- R5. The PR must reference `https://github.com/garethpaul/garethpaul.com/issues/3`.

## Implementation Unit

### U1. Environment-Backed Const Module

- **Goal:** Add `const.py` with environment-backed values, safe placeholder defaults, README documentation, and focused tests for default/override behavior.
- **Files:** `const.py`, `const_tests.py`, `README.md`
- **Test Scenarios:** Clean environment imports `const`, all referenced names exist, defaults contain no secrets, and environment variables override defaults.
- **Verification:** `python3 const_tests.py`, `python3 -m py_compile const.py const_tests.py base.py glass.py instagram.py map.py picasa.py`, `git diff --check`, and `rg -n "GARETHPAUL_|map_api_key|glass_api|picasa_api|instagram_access_token" const.py const_tests.py README.md`.

## Risks

- API endpoints that need real upstream data still require deploy-time environment variables. The safe defaults are intended to make imports and local setup deterministic without exposing secrets.
