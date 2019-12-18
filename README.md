[Feedodon](https://feedodon.rkd.pw/) is a bridge to view Freefeed posts
from your `<SARCASM>`favourite Mastodon`</SARCASM>` client.

If you just want to use it, enter `feedodon.rkd.pw` as Mastodon instance
in your client and paste your Freefeed app token into the authorization
form.

## Run

If you don't trust my server you can host this bridge yourself, easiest
way is Docker of course.

```
docker build -t feedodon .
docker run -p 8000:8000 feedodon
```

You'll need to run it behind a reverse proxy with SSL because that's
what almost all Mastodon clients expect.

I'm running it on [Dokku](http://dokku.viewdocs.io/dokku/) with very
little effort (just created an app, applied letsencrypt, pushed and voila).

## Develop

You need pipenv to set up the project, then

```
pipenv run python manage.py runserver
```

Again, most Mastodon clients won't work on non-standard ports and
without SSL butt you can make requests manually with curl:

```
curl -H 'Authorization: Bearer MY_APP_TOKEN' 'http://127.0.0.1:8000/api/v1/statuses/28'
```

You _don't have to_ go through OAuth to use the API.

## Features

- Home feed
- Comments
- Posting
- Commenting
- Likes/unlikes

Tested with:

- [Twidere](https://github.com/TwidereProject/Twidere-Android) supports
_both_ Twitter and Mastodon, it's even merging feeds together!
- [Musky](https://github.com/StephenVivash/Musky) (all other
[Tusky](https://tusky.app/) forks should work as well)

Reports for iOS, desktop, etc clients welcome!

## Known issues

- Home feed is only sorted by _createdAt_ because Mastodon clients cache
feed heavily and rely on status ordering for pagination
- "Reblog" doesn't map onto Freefeed API so it will always fail
- Public timeline doesn't map onto Freefeed API so it will always fail

## TODO

- notifications
- uploads
- Index page (redirect to github?)
- proper DB
- docker-compose
    - traefik
    - ssl
    - db
- smaller docker image
- tests
