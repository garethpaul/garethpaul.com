#!/usr/bin/env python

import main
import urllib2
import json
import const
from base import Base

class GlassHandler(Base):
  def get(self):
    result = urllib2.urlopen(const.glass_api).read()
    self.response.headers['Content-Type'] = 'application/json'
    data = json.loads(result)
    self.response.out.write(json.dumps(data))
