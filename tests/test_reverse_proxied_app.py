from mock import Mock
from unittest2 import TestCase

from proxyprefix.wsgi import ReverseProxiedApp


class TestReverseProxiedApp(TestCase):
    def setUp(self):
        self.environ = {'SCRIPT_NAME': '/script'}
        self.start_response = Mock()

        self.inner_app = Mock()
        self.proxied_app = ReverseProxiedApp(self.inner_app)

    def test_it_calls_the_wrapped_application(self):
        response = self.proxied_app(self.environ, self.start_response)
        self.inner_app.assert_called_with(self.environ, self.start_response)
        self.assertEqual(response, self.inner_app.return_value)

    def test_it_does_not_alter_SCRIPT_NAME_if_no_HTTP_X_FORWARDED_PREFIX(self):
        self.proxied_app(self.environ, self.start_response)
        self.assertEqual(self.environ['SCRIPT_NAME'], '/script')

    def test_it_prefixes_SCRIPT_NAME_with_HTTP_X_FORWARDED_PREFIX(self):
        self.environ['HTTP_X_FORWARDED_PREFIX'] = 'prefix'
        self.proxied_app(self.environ, self.start_response)
        self.assertEqual(self.environ['SCRIPT_NAME'], '/prefix/script')
