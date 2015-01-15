# OwnYourCheckin

Watches for your Facebook checkins and copies them to your WordPress blog. A
form of automated [PESOS](http://indiewebcamp.com/PESOS). Similar to and
inspired by [OwnYourGram](http://ownyourgram.com/).
[More background.](https://snarfed.org/indie-checkin-flow#OwnYourCheckin)

This is _not_ easy for the average user to set up. It would take a lot more work
to make it a fully usable service like OwnYourGram. You can definitely get it up
and running for yourself if you're not afraid to dive into technical details,
though!

Uses Facebook's
[Real Time Updates](https://developers.facebook.com/docs/graph-api/real-time-updates/v2.2#receiveupdates)
and the [WordPress.com REST API](https://developer.wordpress.com/docs/api/)
(available to self-hosted blogs
[via Jetpack](http://jetpack.me/support/json-api/)).

TODO: If the checkin includes a picture, this "attaches" it to the WordPress
post, which injects the `<img>` tag for it _above_ the post body. Change that so
it ends up below the post body.


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

1. Get a Facebook access token for your own user with the `offline_access`,
`read_stream`, and `user_photos` scopes and put it in a file called
`facebook_access_token` in the repo root dir.
<br /><br />
If you have one lying around, for any app, great! I used mine from
[Bridgy](https://www.brid.gy/). Otherwise, you'll have to generate one, and I
haven't yet found a good manual/interactive way. (The Graph API Explorer doesn't
let you ask for `offline_access`. :/)

1. Create an [App Engine](http://appengine.google.com/) app, replace
`ownyourcheckin` in `app.yaml` with your app id, and deploy.

1. [Subscribe to Real Time Updates](https://developers.facebook.com/docs/graph-api/reference/v2.2/app/subscriptions#publish)
for your own Facebook posts with this command. Fill in APP_ID and ACCESS_TOKEN and
replace `ownyourcheckin` with your App Engine app id.

```shell
curl https://graph.facebook.com/v2.2/APP_ID/subscriptions \
  -d 'object=user&fields=feed&callback_url=https://ownyourcheckin.appspot.com/user_feed_update&verify_token=fluffernutter&access_token=ACCESS_TOKEN'
```

...and you're done! Post a checkin on Facebook, and it should automatically
create a new post on your WordPress site.
