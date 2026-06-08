import socket
import urllib2

URL_TIMEOUT_SECONDS = 10


def read_url(url):
	try:
		return urllib2.urlopen(url, timeout=URL_TIMEOUT_SECONDS).read()
	except socket.timeout as exc:
		raise RuntimeError("Timed out fetching URL: {0}: {1}".format(url, exc))
	except urllib2.URLError as exc:
		raise RuntimeError("Failed fetching URL: {0}: {1}".format(url, exc))
