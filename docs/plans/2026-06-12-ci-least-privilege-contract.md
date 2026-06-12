# CI Least-Privilege Contract

status: completed

## Context

The hosted Python matrix already pinned both actions and granted read-only
repository permissions, but checkout still persisted its token for later steps.
The static baseline also checked individual substrings, which could accept a
second YAML key or executable step that overrode the intended safe value.

## Completed Scope

- Disabled checkout token persistence with `persist-credentials: false`.
- Kept immutable action pins, read-only permissions, cancellation, the bounded
  Ubuntu runner, and the Python 3.10/3.12/3.14 matrix.
- Replaced independent substring checks with an exact dependency-free workflow
  contract so duplicate keys, jobs, permissions, actions, or commands fail.
- Documented the hosted gate as credential-free and non-deploying.

## Verification

- `make check`
- mutations adding duplicate permission, checkout, credential, job, action, or
  run keys must fail
- mutations weakening permissions, pins, runner, timeout, or matrix must fail
- `git diff --check`
