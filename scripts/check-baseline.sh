#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

git -C "$ROOT_DIR" ls-files --error-unmatch const.py >/dev/null

if git -C "$ROOT_DIR" check-ignore -q const.py; then
  printf '%s\n' "const.py must be tracked, not ignored." >&2
  exit 1
fi

for name in \
  GARETHPAUL_MAP_API_KEY \
  GARETHPAUL_GLASS_URL \
  GARETHPAUL_GEOCODE_KEY \
  GARETHPAUL_MAP_API_URL \
  GARETHPAUL_GLASS_API_URL \
  GARETHPAUL_PICASA_API_URL \
  GARETHPAUL_INSTAGRAM_ID \
  GARETHPAUL_INSTAGRAM_ACCESS_TOKEN
do
  grep -q "$name" "$ROOT_DIR/const.py"
  grep -q "$name" "$ROOT_DIR/README.md"
done

printf '%s\n' "garethpaul.com const configuration baseline checks passed."
