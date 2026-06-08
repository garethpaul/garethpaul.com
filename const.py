#!/usr/bin/env python

"""
Runtime configuration for the public site.

Values come from environment variables so a clean checkout can import the app
without committing private API keys or personal feed URLs.
"""

import os


def _env(name, default=""):
	return os.environ.get(name, default)


map_api_key = _env("GARETHPAUL_MAP_API_KEY")
geocode_key = _env("GARETHPAUL_GEOCODE_KEY")
instagram_id = _env("GARETHPAUL_INSTAGRAM_ID")
instagram_access_token = _env("GARETHPAUL_INSTAGRAM_ACCESS_TOKEN")

glass_url = _env("GARETHPAUL_GLASS_URL", "/api/glass")
glass_api = _env("GARETHPAUL_GLASS_API_URL", "https://example.com/glass.json")
picasa_api = _env("GARETHPAUL_PICASA_API_URL", "https://example.com/picasa.json")
map_api = _env("GARETHPAUL_MAP_API_URL", "https://example.com/location.json")
