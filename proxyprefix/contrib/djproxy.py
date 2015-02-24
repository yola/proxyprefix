class XForwardedPrefix(object):
    """Add an X-Forwarded-Prefix header to the djproxy upstream request.

    For enabling proxyprefix behavior during local development (where you may
    not have apache/ngingx/whatever passing the header for you).

    """

    def process_request(self, proxy, request, **kwargs):
        for prefix, url in proxy.reverse_urls:
            if request.path.startswith(prefix):
                kwargs['headers']['X-Forwarded-Prefix'] = prefix
                break

        return kwargs
