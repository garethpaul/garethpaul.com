#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
MAP="$ROOT_DIR/map.py"

if grep -Fq 'http://api.openweathermap.org' "$MAP"; then
  printf '%s\n' "map.py must not use the plain-HTTP OpenWeatherMap endpoint." >&2
  exit 1
fi

if ! grep -Fq 'https://api.openweathermap.org/data/2.5/weather' "$MAP"; then
  printf '%s\n' "map.py must use the HTTPS OpenWeatherMap endpoint." >&2
  exit 1
fi

printf '%s\n' "garethpaul.com HTTPS endpoint baseline checks passed."
