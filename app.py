"""OwnYourCheckin: handler for Facebook Real Time Update for /user/feed.

https://developers.facebook.com/docs/graph-api/real-time-updates/v2.2#receiveupdates

Creates and publishes a new WordPress post via the JSON API. Requires Jetpack
for self-hosted WordPress.

test command line:

curl localhost:8080/user_feed_update \
  -d '{"object":"user","entry":[{"changed_fields":["feed"]}]}'
"""

__author__ = ['Ryan Barrett <ownyourcheckin@ryanb.org>']

import datetime
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

    if (req.get('object') != 'user' or
        'feed' not in req.get('entry', [{}])[0].get('changed_fields', [])):
      return

    # load the user's recent posts
    # TODO: switch to a-u so we can use render_content, etc
    url = 'https://graph.facebook.com/me/feed?access_token=' + FACEBOOK_ACCESS_TOKEN
    feed = self.urlopen_json(url)

    # look for a checkin within the last day
    for post in feed.get('data', []):
      # both facebook and app engine timestamps default to UTC
      place = post.get('place')
      created = post.get('created_time')
      if (place and created and
          datetime.datetime.strptime(created, '%Y-%m-%dT%H:%M:%S+0000') >=
          datetime.datetime.now() - datetime.timedelta(days=1)):
        logging.info('Found checkin:\n%s', json.dumps(post, indent=2))
        break
    else:
      logging.info('No checkin found within the last day. Aborting.')
      return

    # TODO: store in datastore

    post_url = 'https://www.facebook.com/%s/posts/%s' % tuple(post['id'].split('_'))
    args = {'content': """\
<p>%s</p>
<blockquote class="h-as-checkin">
At <a class="h-card p-location" href="https://www.facebook.com/%s">%s</a>.
</blockquote>
<a class="u-syndication" href="%s"></a>
""" % (post.get('message'), place['id'], place['name'], post_url)}

    url = ('https://public-api.wordpress.com/rest/v1.1/sites/%s/posts/new' %
           WORDPRESS_SITE_DOMAIN)
    data = {'content': content,
            # 'media_urls[]': '',
           }
    resp = self.urlopen_json(url, data=urllib.urlencode(data))
    logging.info('Response:\n', url, json.dumps(resp, indent=2))


  def urlopen_json(self, *args, **kwargs):
    logging.info('Fetching %s with args %s', args, kwargs)
    try:
      resp = urllib2.urlopen(*args, **kwargs).read()
      return json.loads(resp)
    except urllib2.URLError, e:
      logging.error(e.reason)
      raise
    except ValueError, e:
      logging.error('Non-JSON response: %s', resp)
      raise


application = webapp2.WSGIApplication(
  [('/user_feed_update', UpdateHandler),
   ], debug=False)
