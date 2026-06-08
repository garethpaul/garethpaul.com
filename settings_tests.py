import importlib
import os
import sys
import types
import unittest


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


class SettingsTest(unittest.TestCase):
	def tearDown(self):
		sys.modules.pop("settings", None)
		sys.modules.pop("const", None)
		for _name, env_name in CONFIG_VALUES:
			os.environ.pop(env_name, None)

	def load_settings(self):
		sys.modules.pop("settings", None)
		return importlib.import_module("settings")

	def set_env_values(self, prefix):
		for name, env_name in CONFIG_VALUES:
			os.environ[env_name] = "{0}-{1}".format(prefix, name)

	def test_loads_values_from_environment(self):
		self.set_env_values("env")

		settings = self.load_settings()

		self.assertEqual(settings.map_api_key, "env-map_api_key")
		self.assertEqual(settings.instagram_access_token, "env-instagram_access_token")

	def test_local_const_values_take_precedence(self):
		self.set_env_values("env")
		local_const = types.ModuleType("const")
		for name, _env_name in CONFIG_VALUES:
			setattr(local_const, name, "local-{0}".format(name))
		sys.modules["const"] = local_const

		settings = self.load_settings()

		self.assertEqual(settings.map_api_key, "local-map_api_key")
		self.assertEqual(settings.geocode_key, "local-geocode_key")

	def test_missing_values_raise_clear_error(self):
		with self.assertRaisesRegex(RuntimeError, "GARETHPAUL_MAP_API_KEY"):
			self.load_settings()


if __name__ == "__main__":
	unittest.main()
