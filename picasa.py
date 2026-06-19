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

try:
  STRING_TYPES = (basestring,)
except NameError:
  STRING_TYPES = (str,)


def picasa_entries(data):
  """Return Picasa entries only from the expected nested container shapes."""
  feed = data.get('feed')
  if not isinstance(feed, dict):
    return []
  entries = feed.get('entry', [])
  if not isinstance(entries, list):
    return []
  return entries


def picasa_entry_src(entry):
  """Return an image source only when a Picasa entry has the expected shape."""
  if not isinstance(entry, dict):
    return None
  content = entry.get('content')
  if not isinstance(content, dict):
    return None
  source = content.get('src')
  if not isinstance(source, STRING_TYPES):
    return None
  try:
    return require_https_url(source, "Picasa image source")
  except ValueError:
    return None


class PicasaHandler(Base):
  def get(self):
    """ work as a proxy for the glass images api """
    data = read_json_object(require_https_url(const.picasa_api, "picasa_api"))
    self.response.headers['Content-Type'] = 'application/json'
    entries = picasa_entries(data)
    images = []
    for i in entries:
      img_src = picasa_entry_src(i)
      if img_src:
        images.append(img_src)
    images.reverse()
    self.response.out.write(json.dumps({"data": images}))
