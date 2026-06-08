#!/usr/bin/env bash
set -euo pipefail

if grep -R "access_token=" -n instagram.py; then
  echo "instagram.py must not hand-build access_token query strings" >&2
  exit 1
fi

grep -q "urllib.urlencode" instagram.py
grep -q "def instagram_recent_media_url" instagram.py
grep -q "urllib2.urlopen(instagram_recent_media_url())" instagram.py

if [ -f docs/bugs/p2-python-access-token-in-url-query-c765eb4838c12375.md ]; then
  echo "resolved Instagram token URL bug file should be removed" >&2
  exit 1
fi

python2 -m py_compile instagram.py 2>/dev/null || python3 - <<'PY'
from pathlib import Path

compile(Path("instagram.py").read_text(), "instagram.py", "exec")
PY
