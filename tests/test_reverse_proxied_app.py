from mock import Mock, patch
from unittest2 import TestCase

from proxyprefix.wsgi import prefix_paths, set_scheme, ReverseProxiedApp


class TestReverseProxiedApp(TestCase):
    def setUp(self):
        prefix_paths_patcher = patch('proxyprefix.wsgi.prefix_paths')
        self.prefix_paths = prefix_paths_patcher.start()
        self.addCleanup(prefix_paths_patcher.stop)

        set_scheme_patcher = patch('proxyprefix.wsgi.set_scheme')
        self.set_scheme = set_scheme_patcher.start()
        self.addCleanup(set_scheme_patcher.stop)

        self.environ = {}
        self.start_response = Mock()
        self.inner_app = Mock()

        self.proxied_app = ReverseProxiedApp(self.inner_app)

    def test_it_calls_the_wrapped_application(self):
        response = self.proxied_app(self.environ, self.start_response)
        self.inner_app.assert_called_with(self.environ, self.start_response)
        self.assertEqual(response, self.inner_app.return_value)

    def test_it_does_not_prefix_paths_if_no_HTTP_X_FORWARDED_PREFIX(self):
        self.proxied_app(self.environ, self.start_response)
        self.assertFalse(self.prefix_paths.called)

    def test_it_prefixes_paths_with_HTTP_X_FORWARDED_PREFIX(self):
        self.environ['HTTP_X_FORWARDED_PREFIX'] = 'prefix'
        self.proxied_app(self.environ, self.start_response)
        self.prefix_paths.assert_called_with(self.environ, 'prefix')

    def test_it_does_not_set_scheme_if_no_HTTP_X_FORWARDED_PROTO(self):
        self.proxied_app(self.environ, self.start_response)
        self.assertFalse(self.set_scheme.called)

    def test_it_sets_scheme_to_HTTP_X_FORWARDED_PROTO(self):
        self.environ['HTTP_X_FORWARDED_PROTO'] = 'http'
        self.proxied_app(self.environ, self.start_response)
        self.set_scheme.assert_called_with(self.environ, 'http')


class TestPrefixPaths(TestCase):
    """prefix_paths(environ, prefix)"""

    def setUp(self):
        self.environ = {'SCRIPT_NAME': '/script', 'SCRIPT_URL': '/scripturl'}
        prefix_paths(self.environ, 'prefix')

    def test_it_prefixes_SCRIPT_NAME_with_prefix(self):
        self.assertEqual(self.environ['SCRIPT_NAME'], '/prefix/script')

    def test_it_prefixes_empty_SCRIPT_NAME_with_prefix(self):
        self.environ['SCRIPT_NAME'] = ''
        prefix_paths(self.environ, 'prefix')
        self.assertEqual(self.environ['SCRIPT_NAME'], '/prefix/')

    def test_it_removes_SCRIPT_URL_if_present(self):
        # see proxyprefix.wsgi.prefix_paths for why we do this
        self.environ['SCRIPT_URL'] = '/script/url'
        prefix_paths(self.environ, 'prefix')
        self.assertFalse(self.environ['SCRIPT_URL'])


class TestSetScheme(TestCase):
    """set_scheme(environ, scheme)"""

    def setUp(self):
        self.environ = {}

    def test_sets_wsgi_url_scheme_to_https_if_scheme_is_https(self):
        set_scheme(self.environ, 'https')
        self.assertEqual(self.environ['wsgi.url_scheme'], 'https')

    def test_sets_wsgi_url_scheme_to_http_if_scheme_is_not_https(self):
        set_scheme(self.environ, 'foo')
        self.assertEqual(self.environ['wsgi.url_scheme'], 'http')
