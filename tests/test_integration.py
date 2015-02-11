from unittest2 import TestCase

from proxyprefix.wsgi import ReverseProxiedApp
from tests.fake_app import app


class TestIntegrationWithFakeApp(TestCase):
    def setUp(self):
        self.orig_wsgi_app = app.wsgi_app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        app.wsgi_app = self.orig_wsgi_app

    def get_path(self, headers=None):
        return self.client.get('/show_path', headers=headers).data

    def test_unwrapped_app_does_not_alter_path(self):
        self.assertEqual(self.get_path(), '/show_path')

    def test_wrapped_app_with_no_header_does_not_alter_path(self):
        app.wsgi_app = ReverseProxiedApp(app.wsgi_app)
        self.assertEqual(self.get_path(), '/show_path')

    def test_wrapped_app_prefixes_path_with_HTTP_X_FORWARDED_PREFIX(self):
        app.wsgi_app = ReverseProxiedApp(app.wsgi_app)
        path = self.get_path(headers={'X-Forwarded-Prefix': 'prefix'})
        self.assertEqual(path, '/prefix/show_path')
