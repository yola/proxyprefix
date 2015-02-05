# proxyprefix

Let a reverse proxy know what path it should use as a prefix for links in the
response.

For example, if `client.com` proxies `service.com` at `client.com/service`,
and you make a request like this:

`GET http://client.com/service/widgets`

`service.com` might include a paginated list of widgets in the response with a
`next` URL, but we don't want that URL to look like this:

`http://service.com/widgets/?page=2`

we want it to look like this:

`http://client.com/service/widgets/?page=2`

Most set-ups will handle changing the host using `X-Forwarded-Host`, but how
does the service know to prefix the path with `service`? This package handles
that using a `X-Forwarded-Prefix` header.

This package contains a plugin for django that patches `get_script_name` so that
it prefixes all paths with the `X-Forwarded-Prefix` header if present.

Django can already handle the host part. If you set
[`settings.USE_X_FORWARDED_HOST`][x_forwarded_host] to `True`, you'll be all
set.

## Installation:

`pip install proxyprefix`

Then add `proxyprefix` to your `settings.INSTALLED_APPS`.

## Development:

Install requirements:

`pip install -r requirements.txt`

Run the tests:

`nosetests tests`

Note: if you just run `nosetests` by itself, it will try to import
`proxyprefix` and fail because Django isn't configured.

[x_forwarded_host]: https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-USE_X_FORWARDED_HOST
