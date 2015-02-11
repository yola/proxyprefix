class ReverseProxiedApp(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script = environ['SCRIPT_NAME']
        prefix = environ.get('HTTP_X_FORWARDED_PREFIX')
        if prefix:
            script = '/%s/%s' % (prefix.strip('/'), script.lstrip('/'))
        environ['SCRIPT_NAME'] = script
        return self.app(environ, start_response)
