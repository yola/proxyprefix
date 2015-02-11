# proxyprefix

Let a reverse proxied app know what path it's proxied at. This will allow it
to prefix URL paths accordingly.

This is achieved using a WSGI middleware that prefixes `SCRIPT_NAME` with an
`X-Forwarded-Prefix` header if present.

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

## Usage

Let's say `client.com` is proxying `service.com` at `client.com/service`.

Let's also say we are already handling the host name change using
`X-Forwarded-For` / `X-Forwarded-Host` (this middleware does not alter host
name).

Let's also say `service.com/posts` returns paginated posts with `next` URLs in
the responses:

```
curl -H 'X-Forwarded-Host: client.com' http://service.com/posts
{
    "next": "http://client.com/posts?page=2",
    ...
}
```

That URL will 404, since the posts live at `/service/posts` on the client. If
`service.com` is running the proxyprefix middleware, you can fix this by
making sure your proxy configuration passes a `X-Forwarded-Prefix` header.
For example:

```
curl -H 'X-Forwarded-Host: client.com' -H 'X-Forwarded-Prefix: service` \
http://service.com/posts
{
    "next": "http://client.com/service/posts?page=2",
    ...
}
```

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
