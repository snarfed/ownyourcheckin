"""OwnYourCheckin: handler for Facebook Real Time Update for /user/feed.

https://developers.facebook.com/docs/graph-api/real-time-updates/v2.2#receiveupdates

Creates and publishes a new WordPress post via the JSON API. Requires Jetpack
for self-hosted WordPress.

https://developer.wordpress.com/docs/api/1.1/post/sites/%24site/posts/new/

pseudocode:
optionally check request sha1 signature
fetch post
translate to mf2
post to WP
store in datastore
"""

__author__ = ['Ryan Barrett <ownyourcheckin@ryanb.org>']

import logging
import json
import urllib2

from google.appengine.ext import ndb
import webapp2


def read(filename):
  with open(filename) as f:
    return f.read().strip()

FACEBOOK_APP_ID = read('facebook_app_id')
FACEBOOK_ACCESS_TOKEN = read('facebook_access_token')
FACEBOOK_VERIFY_TOKEN = 'fluffernutter'

WORDPRESS_SITE_DOMAIN = 'snarfed.org'


class UpdateHandler(webapp2.RequestHandler):

  def get(self):
    """Verifies a request from FB to confirm this endpoint.

    https://developers.facebook.com/docs/graph-api/real-time-updates/v2.2#setupget
    """
    logging.info('Verification request: %s', self.request.params)
    if self.request.get('hub.verify_token') == FACEBOOK_VERIFY_TOKEN:
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write(self.request.get('hub.challenge') + '\r\n')

  def post(self):
    """Converts an FB checkin to a new WP post.

    Example request body:

    {"object" : "user",
     "entry" : [{
       "uid" : "10101456587354063",
       "time" : 1421128210,
       "id" : "10101456587354063",
       "changed_fields" : ["feed"],
     }]
    }

    The entry.id field is just an obfuscated form of the user id. So, I have to
    fetch /user/feed each time and keep track of the posts I've seen. :(
    ...or just find the first checkin in the last day, and give up if none (the
    bootstrap case).
    """
    logging.info('Update request: %s', self.request.body)
    req = json.loads(self.request.body)

    if req.get('object') != 'user':
      return

    # resp = urllib2.urlopen(
    #   'https://public-api.wordpress.com/rest/v1.1/sites/%s/posts/new' %
    #   WORDPRESS_SITE_DOMAIN,
    #   data=json.dumps({}))


application = webapp2.WSGIApplication(
  [('/user_feed_update', UpdateHandler),
   ], debug=False)
