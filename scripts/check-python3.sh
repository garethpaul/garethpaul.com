#!/usr/bin/env sh
set -eu

PYTHON=${PYTHON:-python3}

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  printf '%s\n' "Python 3 command not found: $PYTHON (set PYTHON to a Python 3 executable)." >&2
  exit 1
fi

python_major=$("$PYTHON" -c 'import sys; sys.stdout.write(str(sys.version_info[0]))' 2>/dev/null || true)
if [ "$python_major" != "3" ]; then
  printf '%s\n' "Verification requires Python 3: $PYTHON" >&2
  exit 1
fi
