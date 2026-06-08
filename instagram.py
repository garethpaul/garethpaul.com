#!/usr/bin/env python

import main
import urllib2
import urllib
import json
import const
from base import Base

INSTAGRAM_RECENT_MEDIA_URL = "https://api.instagram.com/v1/users/{0}/media/recent"


def instagram_recent_media_url():
	params = urllib.urlencode({"access_token": const.instagram_access_token})
	return "{0}?{1}".format(
		INSTAGRAM_RECENT_MEDIA_URL.format(const.instagram_id),
		params)


class InstagramHandler(Base):
	def get(self):
		result = urllib2.urlopen(instagram_recent_media_url()).read()
		self.response.headers['Content-Type'] = 'application/json'
		data = json.loads(result)
		next_url = data['pagination']['next_url']
		data_2 = json.loads(urllib2.urlopen(next_url).read())
		d = data['data'] + data_2['data']
		self.response.out.write(json.dumps(d))
