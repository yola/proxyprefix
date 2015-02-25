from unittest2 import TestCase

from mock import Mock

from proxyprefix.contrib.djproxy import XForwardedPrefix


class TestXForwardedPrefix(TestCase):

    def setUp(self):
        self.proxy = Mock(reverse_urls=[('/prefix1/', 'http://example.com/a'),
                                        ('/prefix2/', 'http://example.com/b')])
        self.request = Mock(path='/')
        self.middleware = XForwardedPrefix()

    def get_XFP_header(self):
        headers = {}
        self.middleware.process_request(
            self.proxy, self.request, headers=headers)
        return headers.get('X-Forwarded-Prefix')

    def test_does_not_pass_XFP_header_if_path_does_not_start_with_prefix(self):
        self.assertIsNone(self.get_XFP_header())

    def test_passes_XFP_header_if_path_starts_with_prefix(self):
        self.request.path = '/prefix1/'
        self.assertEqual(self.get_XFP_header(), '/prefix1/')

        self.request.path = '/prefix2/foo/bar'
        self.assertEqual(self.get_XFP_header(), '/prefix2/')
