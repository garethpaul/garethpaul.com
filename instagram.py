#!/usr/bin/env python

import main
import urlparse
import urllib
import urllib2
import json
import const
from base import Base, decode_json_object, read_url

INSTAGRAM_RECENT_MEDIA_URL = (
	"https://api.instagram.com/v1/users/" + str(const.instagram_id) + "/media/recent"
)
INSTAGRAM_API_HOST = "api.instagram.com"


def _without_access_token_query(url):
	"""Remove access_token query values before issuing or following API URLs."""
	parts = urlparse.urlsplit(url)
	query = [
		(key, value)
		for key, value in urlparse.parse_qsl(parts.query, keep_blank_values=True)
		if key != "access_token"
	]
	return urlparse.urlunsplit((
		parts.scheme,
		parts.netloc,
		parts.path,
		urllib.urlencode(query),
		parts.fragment,
	))


def require_instagram_api_url(url):
	"""Return only HTTPS Instagram API URLs before adding bearer credentials."""
	parts = urlparse.urlsplit(url or "")
	if parts.scheme != "https" or parts.netloc.lower() != INSTAGRAM_API_HOST:
		raise ValueError("Instagram API URL must use https://api.instagram.com")
	return url


def instagram_request(url):
	api_url = require_instagram_api_url(_without_access_token_query(url))
	request = urllib2.Request(api_url)
	request.add_header("Authorization", "Bearer " + const.instagram_access_token)
	return read_url(request)


def instagram_json(url):
	return decode_json_object(instagram_request(url))


def instagram_page(data):
	"""Return pagination and media only from the expected container shapes."""
	pagination = data.get('pagination', {})
	if not isinstance(pagination, dict):
		pagination = {}
	media = data.get('data', [])
	if not isinstance(media, list):
		media = []
	return pagination.get('next_url'), media


class InstagramHandler(Base):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		data = instagram_json(INSTAGRAM_RECENT_MEDIA_URL)
		next_url, d = instagram_page(data)
		if next_url:
			data_2 = instagram_json(next_url)
			_, second_page = instagram_page(data_2)
			d = d + second_page
		self.response.out.write(json.dumps(d))
