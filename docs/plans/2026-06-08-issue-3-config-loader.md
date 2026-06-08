# Issue 3 Config Loader

## Issue

`garethpaul/garethpaul.com#3` reports that app modules import `const`, but a
clean checkout does not include `const.py` or a tracked example.

## Plan

- Keep ignored local `const.py` support for existing developer secrets.
- Add tracked `settings.py` that loads values from local `const.py` or
  `GARETHPAUL_*` environment variables.
- Update app modules to import `settings as const`.
- Add `const.py.example` and README configuration instructions.
- Add focused tests for environment loading, local const precedence, and clear
  missing-configuration errors.

## Verification

- `python3 settings_tests.py`
- `python3 -m py_compile settings.py settings_tests.py`
- `scripts/check-baseline.sh`
- `git diff --check`
