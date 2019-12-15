This is source of https://feedodon.rkd.pw/

## Run

Easiest way to run service on your host is Docker of course.

```
docker build -t feedodon .
docker run -p 8000:8000 feedodon
```

You'll need to run it behind a reverse proxy with SSL because that's
what almost all Mastodon clients expect.

I'm running it on [Dokku](http://dokku.viewdocs.io/dokku/) with very
little effort.

## Develop

You need pipenv to set up the project, then

```
pipenv run python manage.py runserver
```

Again, most Mastodon clients won't work on non-standard ports and
without SSL.

## TODO

- user timelines
- posting
- commenting
- notifications
- proper DB
- docker-compose
    - traefik
    - ssl
    - db
- tests
