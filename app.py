"""OwnYourCheckin: handler for Facebook Real Time Update for /user/feed.

https://developers.facebook.com/docs/graph-api/real-time-updates/v2.2#receiveupdates

pseudocode:
optionally check request sha1 signature
fetch post
translate to mf2
post to WP
store in datastore
"""

__author__ = ['Ryan Barrett <ownyourcheckin@ryanb.org>']

import datetime
import itertools
import json
import urlparse

import appengine_config

# need to import modules with model class definitions, e.g. facebook, for
# template rendering.
from activitystreams import facebook
from activitystreams.oauth_dropins.webutil import util

from google.appengine.ext import ndb

FACEBOOK_ACCESS_TOKEN = appengine_config.read('facebook_access_token')


class UpdateHandler(util.Handler):

  def post(self):
    pass


application = webapp2.WSGIApplication(
  [('/user_feed_update', UpdateHandler),
   ], debug=appengine_config.DEBUG)
