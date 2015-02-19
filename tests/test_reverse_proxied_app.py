from mock import Mock, patch
from unittest2 import TestCase

from proxyprefix.wsgi import prefix_paths, ReverseProxiedApp


class TestReverseProxiedApp(TestCase):
    def setUp(self):
        self.prefix_paths_patcher = patch('proxyprefix.wsgi.prefix_paths')
        self.prefix_paths = self.prefix_paths_patcher.start()
        self.addCleanup(self.prefix_paths_patcher.stop)

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
