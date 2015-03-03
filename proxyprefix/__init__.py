"""WSGI middleware to prefix SCRIPT_NAME with X-Forwarded-Prefix header.

For services behind a reverse proxy so their URLs contain the proxied path.

"""

__version__ = '0.1.1'
