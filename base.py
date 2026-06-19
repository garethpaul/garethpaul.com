#!/usr/bin/env python

"""

BASE HANDLER FOR REQUESTS

"""

from google.appengine.api import memcache
import webapp2
import jinja2
import const
import json
import urlparse
import urllib2


HTTP_TIMEOUT_SECONDS = 10
MAX_PROVIDER_RESPONSE_BYTES = 1024 * 1024


class RejectRedirectHandler(urllib2.HTTPRedirectHandler):
  """Refuse provider redirects before request headers can be forwarded."""
  def redirect_request(self, req, fp, code, msg, headers, newurl):
    return None


PROVIDER_OPENER = urllib2.build_opener(RejectRedirectHandler())

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def require_https_url(url, label):
  """Return a private endpoint URL only when it is configured safely."""
  parsed = urlparse.urlsplit(url or "")
  if (parsed.scheme != "https" or not parsed.netloc or
      parsed.username or parsed.password or parsed.fragment):
    raise ValueError("%s must use an HTTPS URL with a host and no embedded credentials or fragment" % label)
  return url


def open_url(url_or_request):
  """Open an outbound request with the shared provider deadline."""
  return PROVIDER_OPENER.open(url_or_request, timeout=HTTP_TIMEOUT_SECONDS)


def read_url(url_or_request):
  """Read and close a provider response within the shared payload limit."""
  response = open_url(url_or_request)
  try:
    payload = response.read(MAX_PROVIDER_RESPONSE_BYTES + 1)
  finally:
    response.close()
  if len(payload) > MAX_PROVIDER_RESPONSE_BYTES:
    raise ValueError("Provider response exceeds %d bytes" % MAX_PROVIDER_RESPONSE_BYTES)
  return payload


def decode_json_object(payload):
  """Decode provider JSON and require a top-level object."""
  payload = json.loads(payload)
  if not isinstance(payload, dict):
    raise ValueError("Provider JSON response must be an object")
  return payload


def read_json_object(url_or_request):
  """Read bounded provider JSON and require a top-level object."""
  return decode_json_object(read_url(url_or_request))


class Base(webapp2.RequestHandler):
  def jsonify(self, payload):
    """
    Function for dealing with JSON e.g. self.jsonify({"job": "dev_advocate"})
    Args:
      payload = the json object
    Returns:
      response out to the web request handler
    """
    payload = json.dumps(payload)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(payload)

  def render(self, name):
    """
    Render templates e.g. self.render("index.html")
    """
    template = JINJA_ENVIRONMENT.get_template(name + '.html')
    data = {
      "map_api_key": const.map_api_key,
      "glass_url": require_https_url(const.glass_url, "glass_url"),
    }
    self.response.write(template.render(data))
