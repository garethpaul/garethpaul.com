#!/usr/bin/env python

import main
import urllib2
import json
import const
from base import Base

class ApiHandler(Base):
	def get(self):
		result = urllib2.urlopen(const.map_api).read()
		lng = json.loads(result)['lng']
		lat = json.loads(result)['lat']
		# fuzzy stuff for map
		# you need privacy in this world
		lat = "{0:.2f}".format(float(lat))
		lng = "{0:.2f}".format(float(lng))
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps({"lat": lat, "lng": lng}))
