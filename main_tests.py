import importlib
import os
import sys
import types
import unittest


class FakeWSGIApplication(object):
	def __init__(self, routes, debug=False):
		self.routes = routes
		self.debug = debug


class FakeBase(object):
	def render(self, _template):
		pass


def install_fake_dependencies():
	google = types.ModuleType('google')
	appengine = types.ModuleType('google.appengine')
	api = types.ModuleType('google.appengine.api')
	ext = types.ModuleType('google.appengine.ext')
	sys.modules['google'] = google
	sys.modules['google.appengine'] = appengine
	sys.modules['google.appengine.api'] = api
	sys.modules['google.appengine.api.users'] = types.ModuleType(
		'google.appengine.api.users'
	)
	sys.modules['google.appengine.ext'] = ext
	sys.modules['google.appengine.ext.ndb'] = types.ModuleType(
		'google.appengine.ext.ndb'
	)

	webapp2 = types.ModuleType('webapp2')
	webapp2.WSGIApplication = FakeWSGIApplication
	sys.modules['webapp2'] = webapp2

	base = types.ModuleType('base')
	base.Base = FakeBase
	sys.modules['base'] = base

	for name, handler in (
		('map', 'ApiHandler'),
		('instagram', 'InstagramHandler'),
		('glass', 'GlassHandler'),
		('picasa', 'PicasaHandler'),
	):
		module = types.ModuleType(name)
		setattr(module, handler, object)
		sys.modules[name] = module


def load_main():
	sys.modules.pop('main', None)
	install_fake_dependencies()
	return importlib.import_module('main')


class MainDebugTest(unittest.TestCase):
	def setUp(self):
		self.original_debug = os.environ.get('GARETHPAUL_DEBUG')

	def tearDown(self):
		if self.original_debug is None:
			os.environ.pop('GARETHPAUL_DEBUG', None)
		else:
			os.environ['GARETHPAUL_DEBUG'] = self.original_debug
		sys.modules.pop('main', None)

	def test_debug_is_disabled_by_default(self):
		os.environ.pop('GARETHPAUL_DEBUG', None)

		main = load_main()

		self.assertFalse(main.app.debug)

	def test_debug_requires_explicit_truthy_env(self):
		os.environ['GARETHPAUL_DEBUG'] = 'on'

		main = load_main()

		self.assertTrue(main.app.debug)

	def test_debug_rejects_falsey_env(self):
		os.environ['GARETHPAUL_DEBUG'] = 'false'

		main = load_main()

		self.assertFalse(main.app.debug)


if __name__ == '__main__':
	unittest.main()
