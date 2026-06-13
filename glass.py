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
import json
import const
from base import Base, read_json_object, require_https_url

class GlassHandler(Base):
  def get(self):
    """ work as a proxy for the glass images api """
    data = read_json_object(require_https_url(const.glass_api, "glass_api"))
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(data))
