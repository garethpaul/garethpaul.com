#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

direct_calls=$(grep -R "urllib2.urlopen" "$ROOT_DIR"/base.py "$ROOT_DIR"/glass.py "$ROOT_DIR"/instagram.py "$ROOT_DIR"/map.py "$ROOT_DIR"/picasa.py || true)
if [ -n "$direct_calls" ]; then
  printf '%s\n' "Python modules must use http_client.read_url instead of direct urllib2.urlopen." >&2
  printf '%s\n' "$direct_calls" >&2
  exit 1
fi

if ! grep -Fq "URL_TIMEOUT_SECONDS = 10" "$ROOT_DIR/http_client.py"; then
  printf '%s\n' "http_client.py must define an explicit URL timeout." >&2
  exit 1
fi

if ! grep -Fq "urllib2.urlopen(url, timeout=URL_TIMEOUT_SECONDS)" "$ROOT_DIR/http_client.py"; then
  printf '%s\n' "http_client.py must pass the timeout to urllib2.urlopen." >&2
  exit 1
fi

for file in glass.py instagram.py map.py picasa.py; do
  if ! grep -Fq "from http_client import read_url" "$ROOT_DIR/$file"; then
    printf '%s\n' "$file must import read_url." >&2
    exit 1
  fi
done

printf '%s\n' "garethpaul.com timeout baseline checks passed."
