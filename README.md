# ownyourcheckin
http://ownyourgram.com/ for Facebook checkins

[More background.](https://snarfed.org/indie-checkin-flow#OwnYourCheckin)
Uses Facebook's
[Real Time Updates](https://developers.facebook.com/docs/graph-api/real-time-updates/v2.2#receiveupdates).


Setup
---

1. Clone this repo.

1. [Create a Facebook app](https://developers.facebook.com/quickstarts/?platform=web).

1. Open the
[Graph API Explorer](https://developers.facebook.com/tools/explorer/), select
your app from the _Application_ drop-down, click _Get Access Token_, click
_Extended Permissions_, check _read\_stream_, and click _Get Access Token_. Copy
the access token into a file called `facebook_access_token` in the repo root
dir.

1. TODO get wordpress access token

1. Deploy this app, on [App Engine](http://appengine.google.com/) or wherever.

1. [Subscribe to Real Time Updates](https://developers.facebook.com/docs/graph-api/reference/v2.2/app/subscriptions#publish)
for your own Facebook posts with this command. Fill in APP_ID and ACCESS_TOKEN and
replace `ownyourcheckin.appspot.com` with the domain where you deployed this app.

```shell
curl https://graph.facebook.com/v2.2/APP_ID/subscriptions \
  -d 'object=user&callback_url=http://ownyourcheckin.appspot.com/user_feed_update&fields=feed&verify_token=fluffernutter&access_token=ACCESS_TOKEN'
```

...and you're done! Post a checkin on Facebook, and it should automatically
create a new post on your WordPress site.
