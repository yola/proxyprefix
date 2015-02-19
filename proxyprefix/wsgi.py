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
    script = environ.get('SCRIPT_NAME', '/')
    environ['SCRIPT_NAME'] = '/%s/%s' % (prefix.strip('/'), script.lstrip('/'))

    # SCRIPT_URL is an apache-specific mod_rewrite variable.  If it exists,
    # Django will try to extract the script name from it, instead of looking at
    # the SCRIPT_NAME env var. But the way Django does this is buggy: it
    # removes len(PATH_INFO) chars from the end of SCRIPT_URL, but PATH_INFO is
    # not always a substring of SCRIPT_URL. Since we are forcing SCRIPT_NAME
    # here anyway, we can remove SCRIPT_URL to simplify things and get around
    # this django quirk:
    if environ.get('SCRIPT_URL'):
        environ['SCRIPT_URL'] = ''
