#!/usr/bin/env python

"""
Functions:

get_weather - service for finding weather
get_address - service for finding address
get_latlng - service for finding lat and lng
get_data - service for combining get_weather, get_address, get_latlng

Classes:

ApiHandler:
	get() - a GET request on the URL /api/map

"""

from google.appengine.api import memcache
import main
import urllib2
import json
import cache
import const
from base import Base


def get_weather(lat,lng):
	"""
	Function: finding weather utilizes opeweathermap.org
	Args:
		lat = latitude of a given location
		lng = longitude of a given location
	Returns:
		Weather dict.
	"""
	weather_url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lng)
	result = urllib2.urlopen(weather_url).read()
	json_data = json.loads(result)
	# json output = http://openweathermap.org/API
	weather = json_data['weather'][0]
	main = json_data['main']
	return dict(main.items() + weather.items())


def get_address(lat,lng):
	"""
	Function: returning an address utilizes Google's geocode APIs
	Args:
		lat = latitude of a given location
		lng = longitue of a given location
	Returns:
		Address dict
	"""
	geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng) + "&key=" + const.geocode_key + "&sensor=true"
	result = urllib2.urlopen(geocode_url).read()
	results = json.loads(result)['results']
	return results[0]['formatted_address']


def get_latlng():
	"""
	Function: provide the latest geo coords.
	Returns:
		Dict object e.g. {"lat": "30.27", "lng": "-97.74"}
	"""
	result = urllib2.urlopen(const.map_api).read()
	lng = json.loads(result)['lng']
	lat = json.loads(result)['lat']
	# fuzzify the map - needed for privacy reasons :-)
	lat = "{0:.2f}".format(float(lat))
	lng = "{0:.2f}".format(float(lng))
	return {"lat": lat, "lng": lng}


def get_data():
	"""
	Function: get data for map request
	Returns: dict object with map information
	"""
	latlng_blob = get_latlng()
	lat = latlng_blob['lat']
	lng = latlng_blob['lng']
	address = get_address(lat, lng)
	weather = get_weather(lat,lng)
	data = {"lat": lat,
					"lng": lng,
					"address": address,
					"status": "ok",
					"meeting": False,
					"weather": weather}
	return data


class ApiHandler(Base):
	def get(self):
		"""
		Function: for a get request for the Map.py api e.g. /api/map
		Returns: json data
		"""
		cachi = cache.check(self.request.url)
		if cachi is None:
			# get_data
			data = get_data()
			# set cache
			memcache.set(key=url_string, value=data, time=8000)
			self.jsonify(data)
		else:
			self.jsonify(cachi)
