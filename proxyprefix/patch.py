from django.core.handlers import base


def patch_get_script_name():
    """Prefix SCRIPT_NAME if X-Forwarded-Prefix header is present.

    This works by hijacking `django.core.handlers.base.get_script_name`.

    We do this so clients that proxy this api will have working URLs in their
    response. For example:

    If client.com proxies sbbe at client.com/sbbe, then:

        GET client.com/sbbe/sites/?page=1

    will respond with `next` URLs like this:

        client.com/sites/?page=2

    which will 404. But if it passes a 'X-Forwarded-Prefix: sbbe' header, they
    will look like this:

        client.com/sbbe/sites/?page=2

    which is correct.

    See: https://github.com/yola/production/issues/1863

    """
    orig_get_script_name = base.get_script_name

    def get_prefixed_script_name(environ):
        script_name = orig_get_script_name(environ)
        prefix = environ.get('HTTP_X_FORWARDED_PREFIX')
        if prefix:
            script_name = "/%s/%s" % (
                prefix.strip('/'), script_name.lstrip('/'))
        return script_name

    base.get_script_name = get_prefixed_script_name
