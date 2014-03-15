from google.appengine.api import memcache

def check(cache_key):
  """
  Function performs cache check
  Returns:
    the cache object or None
  """
  local_cache = memcache.get(cache_key)
  if local_cache is not None:
    return local_cache
  else:
    return None
