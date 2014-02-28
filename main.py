#!/usr/bin/env python

from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import os
import map
import instagram
from base import Base

class MainHandler(Base):
	def get(self):
		self.render("index")

class PictureHandler(Base):
	def get(self):
		self.render('picture')

class ProfileHandler(Base):
	def get(self):
		self.render("profile")

class MapHandler(Base):
	def get(self):
		self.render("map")

class CodeHandler(Base):
	def get(self):
		self.render("code")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
		('/profile', ProfileHandler),
		('/code', CodeHandler),
	  ('/instagram', instagram.InstagramHandler),
	  ('/pictures', PictureHandler),
	  ('/map', MapHandler),
	  ('/api/map', map.ApiHandler)
], debug=True)
