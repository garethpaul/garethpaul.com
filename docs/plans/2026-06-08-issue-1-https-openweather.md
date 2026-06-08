# Issue 1 HTTPS OpenWeatherMap Endpoint

## Issue

`garethpaul/garethpaul.com#1` reports that `map.py` calls the
OpenWeatherMap weather endpoint over plain HTTP.

## Plan

- Switch the runtime OpenWeatherMap URL from HTTP to HTTPS.
- Update the nearby API reference comment to HTTPS.
- Add a source-level baseline script that guards against the old cleartext
  endpoint.

## Verification

- `scripts/check-baseline.sh`
- `rg -n "http://api\\.openweathermap\\.org|https://api\\.openweathermap\\.org|https://openweathermap\\.org/API" map.py scripts/check-baseline.sh`
- `git diff --check`
- `curl -I -L --max-time 15 'https://api.openweathermap.org/data/2.5/weather?lat=0&lon=0'`
