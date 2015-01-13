# ownyourcheckin
http://ownyourgram.com/ for Facebook checkins

[More background.](https://snarfed.org/indie-checkin-flow#OwnYourCheckin)
Uses Facebook's
[Real Time Updates](https://developers.facebook.com/docs/graph-api/real-time-updates/v2.2#receiveupdates).


Setup
---

1. Clone this repo.

1. [Create a new WordPress.com app.](https://developer.wordpress.com/apps/new/)

1. Install the [Jetpack plugin](http://jetpack.me/) in your WordPress site,
connect it to your [WordPress.com](http://wordpress.com/) account, and enable
the [JSON API](http://jetpack.me/support/json-api/) feature.

1. Generate an OAuth token for your WordPress.com app and put it into a file
called `wordpress.com_access_token` in the repo root dir. (Sadly, I haven't found a way
to generate this token manually. I generated mine by running
[oauth-dropins](https://oauth-dropins.appspot.com/) locally and filling in my
app's id and secret in the `wordpress.com_client_id` and
`wordpress.com_client_secret` files.)

1. [Create a Facebook app](https://developers.facebook.com/quickstarts/?platform=web).

1. Open the
[Graph API Explorer](https://developers.facebook.com/tools/explorer/), select
your app from the _Application_ drop-down, and click _Get App Token_. Copy the
token into a file called `facebook_app_token` in the repo root dir.

1. Still in the Graph API Explorer, click _Get Access Token_, click _Extended
Permissions_, check _read\_stream_, and click _Get Access Token_. Copy the token
into a file called `facebook_access_token` in the repo root dir.

1. Deploy this app, on [App Engine](http://appengine.google.com/) or wherever.

1. [Subscribe to Real Time Updates](https://developers.facebook.com/docs/graph-api/reference/v2.2/app/subscriptions#publish)
for your own Facebook posts with this command. Fill in APP_ID and ACCESS_TOKEN and
replace `ownyourcheckin.appspot.com` with the domain where you deployed this app.

```shell
curl https://graph.facebook.com/v2.2/APP_ID/subscriptions \
  -d 'object=user&fields=feed&callback_url=https://ownyourcheckin.appspot.com/user_feed_update&verify_token=fluffernutter&access_token=ACCESS_TOKEN'
```

...and you're done! Post a checkin on Facebook, and it should automatically
create a new post on your WordPress site.

XXX

