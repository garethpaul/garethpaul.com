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
from base import Base, read_url, require_https_url


def picasa_entry_src(entry):
  """Return an image source only when a Picasa entry has the expected shape."""
  if not isinstance(entry, dict):
    return None
  content = entry.get('content')
  if not isinstance(content, dict):
    return None
  return content.get('src')


class PicasaHandler(Base):
  def get(self):
    """ work as a proxy for the glass images api """
    result = read_url(require_https_url(const.picasa_api, "picasa_api"))
    self.response.headers['Content-Type'] = 'application/json'
    data = json.loads(result)
    entries = data.get('feed', {}).get('entry', [])
    images = []
    for i in entries:
      img_src = picasa_entry_src(i)
      if img_src:
        images.append(img_src)
    images.reverse()
    self.response.out.write(json.dumps({"data": images}))
