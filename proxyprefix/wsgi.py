class ReverseProxiedApp(object):
    """WSGI middleware to prefix script name with X-Forwarded-Prefix header."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        prefix = environ.get('HTTP_X_FORWARDED_PREFIX')
        if prefix:
            prefix_paths(environ, prefix)
        return self.app(environ, start_response)


def prefix_paths(environ, prefix):
    """Add a prefix to the URL paths in the environment."""
    for key in ['SCRIPT_NAME', 'SCRIPT_URL']:
        value = environ.get(key, '')
        environ[key] = '/%s/%s' % (prefix.strip('/'), value.lstrip('/'))
