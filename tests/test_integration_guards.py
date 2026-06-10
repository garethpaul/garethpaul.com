import importlib.util
from pathlib import Path
import sys
import types
import unittest
import urllib.parse


ROOT = Path(__file__).resolve().parents[1]


class FakeRequest:
  def __init__(self, url):
    self.full_url = url
    self.headers = {}

  def add_header(self, name, value):
    self.headers[name] = value


class FakeResponse:
  def __init__(self, payload=b"{}"):
    self.payload = payload

  def read(self):
    return self.payload


class FakeJinjaEnvironment:
  def __init__(self, *args, **kwargs):
    pass

  def get_template(self, name):
    raise AssertionError("templates are not rendered by these characterization tests")


def install_legacy_stubs():
  urlparse_module = types.ModuleType("urlparse")
  urlparse_module.urlsplit = urllib.parse.urlsplit
  urlparse_module.urlunsplit = urllib.parse.urlunsplit
  urlparse_module.parse_qsl = urllib.parse.parse_qsl
  sys.modules["urlparse"] = urlparse_module

  urllib_module = types.ModuleType("urllib")
  urllib_module.urlencode = urllib.parse.urlencode
  sys.modules["urllib"] = urllib_module

  urllib2_module = types.ModuleType("urllib2")
  urllib2_module.Request = FakeRequest
  urllib2_module.urlopen = lambda request: FakeResponse()
  sys.modules["urllib2"] = urllib2_module

  const_module = types.ModuleType("const")
  const_module.glass_url = "https://example.com/glass"
  const_module.map_api_key = "map-key"
  const_module.instagram_id = "123"
  const_module.instagram_access_token = "secret-token"
  const_module.picasa_api = "https://example.com/picasa"
  sys.modules["const"] = const_module

  google_module = types.ModuleType("google")
  appengine_module = types.ModuleType("google.appengine")
  api_module = types.ModuleType("google.appengine.api")
  memcache_module = types.ModuleType("google.appengine.api.memcache")
  api_module.memcache = memcache_module
  appengine_module.api = api_module
  google_module.appengine = appengine_module
  sys.modules["google"] = google_module
  sys.modules["google.appengine"] = appengine_module
  sys.modules["google.appengine.api"] = api_module
  sys.modules["google.appengine.api.memcache"] = memcache_module

  webapp2_module = types.ModuleType("webapp2")
  webapp2_module.RequestHandler = object
  sys.modules["webapp2"] = webapp2_module

  jinja2_module = types.ModuleType("jinja2")
  jinja2_module.Environment = FakeJinjaEnvironment
  jinja2_module.FileSystemLoader = lambda path: object()
  sys.modules["jinja2"] = jinja2_module

  sys.modules["main"] = types.ModuleType("main")


def load_module(name, relative_path):
  sys.modules.pop(name, None)
  spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
  module = importlib.util.module_from_spec(spec)
  sys.modules[name] = module
  spec.loader.exec_module(module)
  return module


install_legacy_stubs()
base = load_module("base", "base.py")
instagram = load_module("instagram", "instagram.py")
picasa = load_module("picasa", "picasa.py")


class PrivateEndpointGuardTest(unittest.TestCase):
  def test_require_https_url_accepts_https_url_with_host(self):
    url = "https://example.com/private/path?city=sf"

    self.assertEqual(url, base.require_https_url(url, "map_api"))

  def test_require_https_url_rejects_unsafe_private_endpoint_parts(self):
    unsafe_urls = [
      "http://example.com/private",
      "https:///missing-host",
      "https://user@example.com/private",
      "https://user:pass@example.com/private",
      "https://example.com/private#token",
      "",
      None,
    ]

    for url in unsafe_urls:
      with self.subTest(url=url):
        with self.assertRaises(ValueError):
          base.require_https_url(url, "map_api")


class InstagramGuardTest(unittest.TestCase):
  def test_without_access_token_query_strips_token_and_preserves_other_params(self):
    url = (
      "https://api.instagram.com/v1/users/123/media/recent"
      "?access_token=secret&count=2&empty="
    )

    sanitized = instagram._without_access_token_query(url)

    self.assertNotIn("access_token", sanitized)
    self.assertIn("count=2", sanitized)
    self.assertIn("empty=", sanitized)

  def test_require_instagram_api_url_rejects_non_instagram_destinations(self):
    unsafe_urls = [
      "http://api.instagram.com/v1/users/123/media/recent",
      "https://evil.example/v1/users/123/media/recent",
      "https://api.instagram.com.evil.example/v1/users/123/media/recent",
      "",
      None,
    ]

    for url in unsafe_urls:
      with self.subTest(url=url):
        with self.assertRaises(ValueError):
          instagram.require_instagram_api_url(url)

  def test_instagram_request_uses_sanitized_url_and_authorization_header(self):
    captured = []
    original_urlopen = instagram.urllib2.urlopen
    self.addCleanup(setattr, instagram.urllib2, "urlopen", original_urlopen)

    def fake_urlopen(request):
      captured.append(request)
      return FakeResponse(b"{}")

    instagram.urllib2.urlopen = fake_urlopen

    instagram.instagram_request(
      "https://api.instagram.com/v1/users/123/media/recent"
      "?access_token=query-token&count=2"
    )

    self.assertEqual(1, len(captured))
    self.assertEqual(
      "https://api.instagram.com/v1/users/123/media/recent?count=2",
      captured[0].full_url,
    )
    self.assertEqual("Bearer secret-token", captured[0].headers["Authorization"])


class PicasaGuardTest(unittest.TestCase):
  def test_picasa_entry_src_returns_source_for_expected_entry_shape(self):
    self.assertEqual(
      "https://example.com/image.jpg",
      picasa.picasa_entry_src({"content": {"src": "https://example.com/image.jpg"}}),
    )

  def test_picasa_entry_src_ignores_malformed_entries(self):
    malformed_entries = [
      None,
      [],
      {},
      {"content": None},
      {"content": []},
      {"content": {}},
    ]

    for entry in malformed_entries:
      with self.subTest(entry=entry):
        self.assertIsNone(picasa.picasa_entry_src(entry))


if __name__ == "__main__":
  unittest.main()
