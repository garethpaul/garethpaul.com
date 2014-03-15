#!/usr/bin/env python

import main
import urllib2
import json
import const
from base import Base


def get_address(lat,lng):
	"""
	Utilize Google's Geocode API to return an approximate address
	"""
	geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng) + "&key=" + const.geocode_key + "&sensor=true"
	result = urllib2.urlopen(geocode_url).read()
	results = json.loads(result)['results']
	return results[0]['formatted_address']

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
		address = get_address(lat, lng)
		self.response.out.write(json.dumps({"lat": lat, "lng": lng, "address": address}))
