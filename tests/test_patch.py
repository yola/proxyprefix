from proxyprefix.patch import patch_get_script_name

from unittest2 import TestCase
from mock import patch


class TestPatchGetScriptName(TestCase):
    """patch_get_script_name()"""

    def setUp(self):
        base_patch = patch('proxyprefix.patch.base')
        mocked_base = base_patch.start()
        self.addCleanup(base_patch.stop)

        self.orig_get_script_name = mocked_base.get_script_name
        patch_get_script_name()
        self.patched_get_script_name = mocked_base.get_script_name

    def test_prefixes_script_name_with_prefix_header_if_present(self):
        environ = {'HTTP_X_FORWARDED_PREFIX': 'foo'}
        self.orig_get_script_name.return_value = '/bar'

        script_name = self.patched_get_script_name(environ)

        self.assertEqual(script_name, '/foo/bar')
        self.orig_get_script_name.assert_called_once_with(environ)

    def test_returns_unaltered_script_name_if_no_prefix_header(self):
        environ = {}
        self.orig_get_script_name.return_value = '/bar'

        script_name = self.patched_get_script_name(environ)

        self.assertEqual(script_name, '/bar')
        self.orig_get_script_name.assert_called_once_with(environ)

    def test_handles_leading_slash_in_prefix(self):
        environ = {'HTTP_X_FORWARDED_PREFIX': '/foo'}
        self.orig_get_script_name.return_value = '/bar'

        script_name = self.patched_get_script_name(environ)

        self.assertEqual(script_name, '/foo/bar')
