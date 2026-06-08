#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

if grep -R "^import const$" "$ROOT_DIR"/*.py; then
  printf '%s\n' "Python modules must import settings as const, not const directly." >&2
  exit 1
fi

for file in base.py glass.py instagram.py map.py picasa.py; do
  if ! grep -Fq "import settings as const" "$ROOT_DIR/$file"; then
    printf '%s\n' "$file must import settings as const." >&2
    exit 1
  fi
done

if ! grep -Fq "const.py" "$ROOT_DIR/.gitignore"; then
  printf '%s\n' ".gitignore must keep local const.py secrets out of git." >&2
  exit 1
fi

if [ ! -f "$ROOT_DIR/const.py.example" ]; then
  printf '%s\n' "const.py.example must be tracked as local setup documentation." >&2
  exit 1
fi

if ! grep -Fq "GARETHPAUL_MAP_API_KEY" "$ROOT_DIR/settings.py"; then
  printf '%s\n' "settings.py must load documented environment variables." >&2
  exit 1
fi

if ! grep -Fq "GARETHPAUL_MAP_API_KEY" "$ROOT_DIR/README.md"; then
  printf '%s\n' "README must document required configuration." >&2
  exit 1
fi

printf '%s\n' "garethpaul.com config baseline checks passed."
