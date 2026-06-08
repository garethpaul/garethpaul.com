#!/usr/bin/env python

import main
import json
import const
from http_client import read_url
from base import Base
instagram_url = "https://api.instagram.com/v1/users/" + str(const.instagram_id) + "/media/recent?access_token=" + const.instagram_access_token


class InstagramHandler(Base):
	def get(self):
		result = read_url(instagram_url)
		self.response.headers['Content-Type'] = 'application/json'
		data = json.loads(result)
		next_url = data['pagination']['next_url']
		data_2 = json.loads(read_url(next_url))
		d = data['data'] + data_2['data']
		self.response.out.write(json.dumps(d))
