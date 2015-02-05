from django.test.client import RequestFactory
from unittest2 import TestCase

from tests.fake_app.views import show_path


class TestDjangoRequestWithHeader(TestCase):
    """A Django request with X-Forwarded-Prefix header"""

    def test_includes_prefix_in_url_lookups(self):
        request = RequestFactory().get('/path/')
        request.META['HTTP_X_FORWARDED_PREFIX'] = 'prefix'
        response = show_path(request)
        self.assertEqual(response.content, '/prefix/path/')
