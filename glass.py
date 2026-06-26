#!/usr/bin/env python

"""
Main Handler for GoogleGlass

There is an API that provides a list of images from Glass to be used specifically for this user.
Note:
  settings.py provides the HTTPS endpoint.

"""
import main
import json
import settings as const
import cache
from google.appengine.api import memcache
from base import Base, read_json_object, require_https_url

GLASS_CACHE_KEY = "glass-api-response"
GLASS_CACHE_SECONDS = 300


def get_data():
  data = cache.check(GLASS_CACHE_KEY)
  if data is not None:
    return data

  data = read_json_object(require_https_url(const.glass_api, "glass_api"))
  memcache.set(key=GLASS_CACHE_KEY, value=data, time=GLASS_CACHE_SECONDS)
  return data


class GlassHandler(Base):
  def get(self):
    """ work as a proxy for the glass images api """
    data = get_data()
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(data))
