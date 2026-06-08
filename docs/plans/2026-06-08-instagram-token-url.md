# Instagram Token URL Handling

## Context

Repo-local finding: `docs/bugs/p2-python-access-token-in-url-query-c765eb4838c12375.md`

The legacy Instagram API call requires an access token, but the code stored a fully tokenized URL in a module-level constant using string concatenation.

## Plan

1. Remove the module-level tokenized URL constant.
2. Build the legacy Instagram URL at call time with encoded parameters.
3. Add a source-level baseline check that rejects hand-built `access_token=` URLs and verifies the helper is used.
4. Remove the resolved repo-local bug file.

## Verification

- Run `scripts/check-baseline.sh`.
- Run `git diff --check`.
