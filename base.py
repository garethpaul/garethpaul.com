#!/usr/bin/env python

"""

BASE HANDLER FOR REQUESTS

"""

from google.appengine.api import memcache
import webapp2
import jinja2
import const
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Base(webapp2.RequestHandler):
  def jsonify(self, payload):
    """
    Function for dealing with JSON e.g. self.jsonify({"job": "dev_advocate"})
    Args:
      payload = the json object
    Returns:
      response out to the web request handler
    """
    payload = json.dumps(payload)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(payload)

  def render(self, name):
    """
    Render templates e.g. self.render("index.html")
    """
    template = JINJA_ENVIRONMENT.get_template(name + '.html')
    data = {"map_api_key": const.map_api_key, "glass_url": const.glass_url}
    self.response.write(template.render(data))
