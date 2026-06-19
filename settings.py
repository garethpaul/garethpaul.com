#!/usr/bin/env python

import os


try:
  import const as local_const
except ImportError:
  local_const = None


CONFIG_VALUES = (
  ("map_api_key", "GARETHPAUL_MAP_API_KEY"),
  ("glass_url", "GARETHPAUL_GLASS_URL"),
  ("glass_api", "GARETHPAUL_GLASS_API"),
  ("instagram_id", "GARETHPAUL_INSTAGRAM_ID"),
  ("instagram_access_token", "GARETHPAUL_INSTAGRAM_ACCESS_TOKEN"),
  ("picasa_api", "GARETHPAUL_PICASA_API"),
  ("map_api", "GARETHPAUL_MAP_API"),
  ("geocode_key", "GARETHPAUL_GEOCODE_KEY"),
)


def required_value(name, env_name):
  """Load one required setting from ignored const.py or the environment."""
  if local_const is not None and hasattr(local_const, name):
    value = getattr(local_const, name)
    if value not in (None, ""):
      return value

  value = os.environ.get(env_name)
  if value not in (None, ""):
    return value

  raise RuntimeError(
    "Missing required configuration for %s. Set %s or copy "
    "const.py.example to const.py." % (name, env_name)
  )


for config_name, config_env in CONFIG_VALUES:
  globals()[config_name] = required_value(config_name, config_env)
