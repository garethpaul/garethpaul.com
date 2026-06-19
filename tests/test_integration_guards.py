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
    self.closed = False
    self.read_sizes = []

  def read(self, size=None):
    self.read_sizes.append(size)
    if size is None:
      return self.payload
    return self.payload[:size]

  def close(self):
    self.closed = True


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
  urllib2_module.urlopen = lambda request, timeout=None: FakeResponse()
  sys.modules["urllib2"] = urllib2_module

  const_module = types.ModuleType("const")
  const_module.glass_url = "https://example.com/glass"
  const_module.map_api_key = "map-key"
  const_module.instagram_id = "123"
  const_module.instagram_access_token = "secret-token"
  const_module.picasa_api = "https://example.com/picasa"
  const_module.glass_api = "https://example.com/glass-api"
  const_module.map_api = "https://example.com/map-api"
  const_module.geocode_key = "geocode-key"
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

  def test_open_url_uses_shared_timeout(self):
    captured = []
    original_urlopen = base.urllib2.urlopen
    self.addCleanup(setattr, base.urllib2, "urlopen", original_urlopen)

    def fake_urlopen(request, timeout=None):
      captured.append((request, timeout))
      return FakeResponse()

    base.urllib2.urlopen = fake_urlopen

    request = FakeRequest("https://example.com/provider")
    response = base.open_url(request)

    self.assertIsInstance(response, FakeResponse)
    self.assertEqual(1, len(captured))
    self.assertIs(request, captured[0][0])
    self.assertEqual(base.HTTP_TIMEOUT_SECONDS, captured[0][1])
    self.assertEqual(10, base.HTTP_TIMEOUT_SECONDS)

  def test_read_url_accepts_exact_limit_and_closes_response(self):
    response = FakeResponse(b"x" * base.MAX_PROVIDER_RESPONSE_BYTES)
    original_open_url = base.open_url
    self.addCleanup(setattr, base, "open_url", original_open_url)
    base.open_url = lambda request: response

    payload = base.read_url("https://example.com/provider")

    self.assertEqual(base.MAX_PROVIDER_RESPONSE_BYTES, len(payload))
    self.assertEqual([base.MAX_PROVIDER_RESPONSE_BYTES + 1], response.read_sizes)
    self.assertTrue(response.closed)

  def test_read_url_rejects_oversized_payload_and_closes_response(self):
    response = FakeResponse(b"x" * (base.MAX_PROVIDER_RESPONSE_BYTES + 1))
    original_open_url = base.open_url
    self.addCleanup(setattr, base, "open_url", original_open_url)
    base.open_url = lambda request: response

    with self.assertRaises(ValueError):
      base.read_url("https://example.com/provider")

    self.assertTrue(response.closed)

  def test_read_url_closes_response_when_read_fails(self):
    class FailingResponse(FakeResponse):
      def read(self, size=None):
        raise IOError("read failed")

    response = FailingResponse()
    original_open_url = base.open_url
    self.addCleanup(setattr, base, "open_url", original_open_url)
    base.open_url = lambda request: response

    with self.assertRaises(IOError):
      base.read_url("https://example.com/provider")

    self.assertTrue(response.closed)

  def test_read_json_object_accepts_object_payload(self):
    original_read_url = base.read_url
    self.addCleanup(setattr, base, "read_url", original_read_url)
    base.read_url = lambda request: b'{"status": "ok"}'

    self.assertEqual(
      {"status": "ok"},
      base.read_json_object("https://example.com/provider"),
    )

  def test_read_json_object_rejects_malformed_json(self):
    original_read_url = base.read_url
    self.addCleanup(setattr, base, "read_url", original_read_url)
    base.read_url = lambda request: b'{"status"'

    with self.assertRaises(ValueError):
      base.read_json_object("https://example.com/provider")

  def test_read_json_object_rejects_non_object_json(self):
    original_read_url = base.read_url
    self.addCleanup(setattr, base, "read_url", original_read_url)

    for payload in (b'[]', b'"value"', b'1', b'true', b'null'):
      with self.subTest(payload=payload):
        base.read_url = lambda request, payload=payload: payload
        with self.assertRaises(ValueError):
          base.read_json_object("https://example.com/provider")


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
    original_read_url = instagram.read_url
    self.addCleanup(setattr, instagram, "read_url", original_read_url)

    def fake_read_url(request):
      captured.append(request)
      return b"{}"

    instagram.read_url = fake_read_url

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
  def test_picasa_entries_returns_expected_entry_list(self):
    entries = [{"content": {"src": "https://example.com/image.jpg"}}]

    self.assertEqual(entries, picasa.picasa_entries({"feed": {"entry": entries}}))

  def test_picasa_entries_ignores_malformed_feed_containers(self):
    malformed_payloads = [
      {},
      {"feed": None},
      {"feed": []},
      {"feed": "invalid"},
      {"feed": {}},
      {"feed": {"entry": None}},
      {"feed": {"entry": {}}},
      {"feed": {"entry": "invalid"}},
    ]

    for payload in malformed_payloads:
      with self.subTest(payload=payload):
        self.assertEqual([], picasa.picasa_entries(payload))

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
