import importlib
import os
from pathlib import Path
import sys
import types
import unittest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))


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


class SettingsLoaderTest(unittest.TestCase):
  def setUp(self):
    self.original_env = {
      env_name: os.environ.get(env_name)
      for _name, env_name in CONFIG_VALUES
    }
    sys.modules.pop("settings", None)
    sys.modules.pop("const", None)

  def tearDown(self):
    sys.modules.pop("settings", None)
    sys.modules.pop("const", None)
    for _name, env_name in CONFIG_VALUES:
      if self.original_env[env_name] is None:
        os.environ.pop(env_name, None)
      else:
        os.environ[env_name] = self.original_env[env_name]

  def load_settings(self):
    sys.modules.pop("settings", None)
    return importlib.import_module("settings")

  def set_env_values(self, prefix):
    for name, env_name in CONFIG_VALUES:
      os.environ[env_name] = "%s-%s" % (prefix, name)

  def test_loads_values_from_environment(self):
    self.set_env_values("env")

    settings = self.load_settings()

    self.assertEqual("env-map_api_key", settings.map_api_key)
    self.assertEqual("env-instagram_access_token", settings.instagram_access_token)

  def test_local_const_values_take_precedence_over_environment(self):
    self.set_env_values("env")
    local_const = types.ModuleType("const")
    for name, _env_name in CONFIG_VALUES:
      setattr(local_const, name, "local-%s" % name)
    sys.modules["const"] = local_const

    settings = self.load_settings()

    self.assertEqual("local-map_api_key", settings.map_api_key)
    self.assertEqual("local-geocode_key", settings.geocode_key)

  def test_missing_value_raises_clear_setup_error(self):
    for _name, env_name in CONFIG_VALUES:
      os.environ.pop(env_name, None)

    with self.assertRaisesRegex(RuntimeError, "GARETHPAUL_MAP_API_KEY"):
      self.load_settings()


if __name__ == "__main__":
  unittest.main()
