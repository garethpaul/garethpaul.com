#!/usr/bin/env python

import webapp2
import jinja2
import const

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Base(webapp2.RequestHandler):
  def render(self, name):
    template = JINJA_ENVIRONMENT.get_template(name + '.html')
    data = {"map_api_key": const.map_api_key, "glass_url": const.glass_url}
    self.response.write(template.render(data))
