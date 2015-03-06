# proxyprefix

Let a proxied service know how it should construct URLs in the response.

This is achieved using a WSGI middleware that prefixes `SCRIPT_NAME` with an
`X-Forwarded-Prefix` header if present.

It will also update the WSGI environ to set `wsgi.url_scheme` and `HTTPS`
according to the `X-Forwarded-Proto` header if present.

## Example

Let's say:

`curl https://service.com/posts/`

responds with:

```
{
    "posts": [...],
    "next": "https://service.com/posts/?page=2"
}
```

If we put `service` behind a proxy at `http://client.com/service/`, we want to
make the following changes to that `next` URL:

1. The host name should be `client.com` instead of `service.com`.
2. The protocol should be `http` instead of `https`.
3. The path should start with `/service/`.

If you're using django, you can do all three by setting
`settings.USE_X_FORWARDED_HOST` to `True`, installing the `proxyprefix` WSGI
middleware, and making sure your proxy sends these headers with its request to
`service`:

```
curl \
  --header X-Forwarded-Host: client.com \
  --header X-Forwarded-Proto: http \
  --header X-Forwarded-Prefix: /service/ \
  https://service.com/posts/
```

Which gives you a response with links to the proxy, not the service:

```
{
    "posts": [...],
    "next": "http://client.com/service/posts/?page=2"
}
```

## Installation

```
pip install proxyprefix
```

```python
from proxyprefix.wsgi import ReverseProxiedApp

# flask example:
app.wsgi_app = ReverseProxiedApp(app.wsgi_app)

# django example:
application = ReverseProxiedApp(get_wsgi_application())
```

### Sending `X-Forwarded-*` headers in local development

If you use [djproxy](https://github.com/thomasw/djproxy) to proxy services in
local development, it will send `X-Forwarded-Host` and `X-Forwarded-Proto` for
you. But `X-Forwarded-Prefix` is a non-standard header, so you will need to use
the middleware provided by proxyprefix:

```python
from djproxy.urls import generate_routes

configuration = {
    'service_name': {
        'base_url': 'https://service.com/',
        'prefix': '/service_prefix/',
        'append_middlware': ['proxyprefx.contrib.djproxy.XForwardedPrefix']
    }
}

urlpatterns += generate_routes(configuration)
```

**Middleware support was added in djproxy 2.0.0.**

## Development

Clone the project and install requirements:

```
pip install -r requirements.txt
```

Run the tests with nosetests:

```
nosetests
```

You can lint and test files when they change automatically using
[testtube](https://github.com/thomasw/testtube):

```
stir
```
