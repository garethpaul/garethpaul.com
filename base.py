#!/usr/bin/env python

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Base(webapp2.RequestHandler):
	def render(self, name):
		template = JINJA_ENVIRONMENT.get_template(name + '.html')
		self.response.write(template.render())