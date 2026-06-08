#!/usr/bin/env python

import main
import urllib
import urllib2
import urlparse
import json
import const
from base import Base
instagram_url = "https://api.instagram.com/v1/users/" + str(const.instagram_id) + "/media/recent"


def instagram_request(url):
	parsed = urlparse.urlsplit(url)
	query = urlparse.parse_qsl(parsed.query, keep_blank_values=True)
	query = [(key, value) for key, value in query if key != 'access_token']
	clean_url = urlparse.urlunsplit((
		parsed.scheme,
		parsed.netloc,
		parsed.path,
		urllib.urlencode(query),
		parsed.fragment,
	))
	request = urllib2.Request(clean_url)
	request.add_header('Authorization', 'Bearer ' + const.instagram_access_token)
	return request


class InstagramHandler(Base):
	def get(self):
		result = urllib2.urlopen(instagram_request(instagram_url)).read()
		self.response.headers['Content-Type'] = 'application/json'
		data = json.loads(result)
		next_url = data['pagination']['next_url']
		data_2 = json.loads(urllib2.urlopen(instagram_request(next_url)).read())
		d = data['data'] + data_2['data']
		self.response.out.write(json.dumps(d))
