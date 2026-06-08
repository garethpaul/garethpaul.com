import importlib
import os
import sys
import unittest


CONFIG_NAMES = (
	"GARETHPAUL_MAP_API_KEY",
	"GARETHPAUL_GEOCODE_KEY",
	"GARETHPAUL_INSTAGRAM_ID",
	"GARETHPAUL_INSTAGRAM_ACCESS_TOKEN",
	"GARETHPAUL_GLASS_URL",
	"GARETHPAUL_GLASS_API_URL",
	"GARETHPAUL_PICASA_API_URL",
	"GARETHPAUL_MAP_API_URL",
)


def load_const():
	sys.modules.pop("const", None)
	return importlib.import_module("const")


class ConstConfigTest(unittest.TestCase):
	def setUp(self):
		self.original_values = {
			name: os.environ.get(name)
			for name in CONFIG_NAMES
		}
		for name in CONFIG_NAMES:
			os.environ.pop(name, None)

	def tearDown(self):
		for name, value in self.original_values.items():
			if value is None:
				os.environ.pop(name, None)
			else:
				os.environ[name] = value
		sys.modules.pop("const", None)

	def test_defaults_are_safe_for_clean_checkout_imports(self):
		const = load_const()

		self.assertEqual(const.map_api_key, "")
		self.assertEqual(const.geocode_key, "")
		self.assertEqual(const.instagram_id, "")
		self.assertEqual(const.instagram_access_token, "")
		self.assertEqual(const.glass_url, "/api/glass")
		self.assertEqual(const.glass_api, "https://example.com/glass.json")
		self.assertEqual(const.picasa_api, "https://example.com/picasa.json")
		self.assertEqual(const.map_api, "https://example.com/location.json")

	def test_environment_values_override_defaults(self):
		os.environ["GARETHPAUL_MAP_API_KEY"] = "maps-key"
		os.environ["GARETHPAUL_GEOCODE_KEY"] = "geocode-key"
		os.environ["GARETHPAUL_INSTAGRAM_ID"] = "123"
		os.environ["GARETHPAUL_INSTAGRAM_ACCESS_TOKEN"] = "token"
		os.environ["GARETHPAUL_GLASS_URL"] = "/glass"
		os.environ["GARETHPAUL_GLASS_API_URL"] = "https://feeds.example.test/glass"
		os.environ["GARETHPAUL_PICASA_API_URL"] = "https://feeds.example.test/picasa"
		os.environ["GARETHPAUL_MAP_API_URL"] = "https://feeds.example.test/map"

		const = load_const()

		self.assertEqual(const.map_api_key, "maps-key")
		self.assertEqual(const.geocode_key, "geocode-key")
		self.assertEqual(const.instagram_id, "123")
		self.assertEqual(const.instagram_access_token, "token")
		self.assertEqual(const.glass_url, "/glass")
		self.assertEqual(const.glass_api, "https://feeds.example.test/glass")
		self.assertEqual(const.picasa_api, "https://feeds.example.test/picasa")
		self.assertEqual(const.map_api, "https://feeds.example.test/map")


if __name__ == "__main__":
	unittest.main()
