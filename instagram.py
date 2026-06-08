#!/usr/bin/env python

import main
import urlparse
import urllib
import urllib2
import json
import const
from base import Base

INSTAGRAM_RECENT_MEDIA_URL = (
	"https://api.instagram.com/v1/users/" + str(const.instagram_id) + "/media/recent"
)


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


def instagram_request(url):
	request = urllib2.Request(_without_access_token_query(url))
	request.add_header("Authorization", "Bearer " + const.instagram_access_token)
	return urllib2.urlopen(request)


def instagram_json(url):
	return json.loads(instagram_request(url).read())


class InstagramHandler(Base):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		data = instagram_json(INSTAGRAM_RECENT_MEDIA_URL)
		next_url = data.get('pagination', {}).get('next_url')
		d = data.get('data', [])
		if next_url:
			data_2 = instagram_json(next_url)
			d = d + data_2.get('data', [])
		self.response.out.write(json.dumps(d))
