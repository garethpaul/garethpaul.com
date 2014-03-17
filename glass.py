#!/usr/bin/env python

"""
Main Handler for GoogleGlass

There is an API that provides a list of images from Glass to be used specifically for this user.
Note:
  const.py provides the HTTPS endpoint.

Todo:
  create a cache service to limit HTTP requests to the server.

"""
import main
import urllib2
import json
import const
from base import Base

class GlassHandler(Base):
  def get(self):
    """ work as a proxy for the glass images api """
    result = urllib2.urlopen(const.glass_api).read()
    self.response.headers['Content-Type'] = 'application/json'
    data = json.loads(result)
    self.response.out.write(json.dumps(data))
