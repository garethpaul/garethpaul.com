import importlib
import socket
import sys
import types
import unittest


class FakeResponse(object):
	def __init__(self, body):
		self.body = body

	def read(self):
		return self.body


class FakeUrlError(Exception):
	pass


def install_fake_urllib2(urlopen):
	urllib2 = types.ModuleType("urllib2")
	urllib2.urlopen = urlopen
	urllib2.URLError = FakeUrlError
	sys.modules["urllib2"] = urllib2


def load_http_client():
	sys.modules.pop("http_client", None)
	return importlib.import_module("http_client")


class HttpClientTest(unittest.TestCase):
	def tearDown(self):
		sys.modules.pop("http_client", None)
		sys.modules.pop("urllib2", None)

	def test_read_url_passes_timeout_and_reads_body(self):
		calls = []

		def urlopen(url, timeout=None):
			calls.append((url, timeout))
			return FakeResponse("payload")

		install_fake_urllib2(urlopen)
		http_client = load_http_client()

		self.assertEqual(http_client.read_url("https://example.test"), "payload")
		self.assertEqual(
			calls, [("https://example.test", http_client.URL_TIMEOUT_SECONDS)]
		)

	def test_read_url_wraps_socket_timeouts(self):
		def urlopen(_url, timeout=None):
			raise socket.timeout("stalled")

		install_fake_urllib2(urlopen)
		http_client = load_http_client()

		with self.assertRaisesRegex(RuntimeError, "Timed out fetching URL"):
			http_client.read_url("https://example.test")

	def test_read_url_wraps_url_errors(self):
		def urlopen(_url, timeout=None):
			raise FakeUrlError("unreachable")

		install_fake_urllib2(urlopen)
		http_client = load_http_client()

		with self.assertRaisesRegex(RuntimeError, "Failed fetching URL"):
			http_client.read_url("https://example.test")


if __name__ == "__main__":
	unittest.main()
