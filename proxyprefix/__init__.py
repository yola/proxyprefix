"""Patch Django's `get_script_name` to support X-Forwaded-Prefix header.

Include this module in `INSTALLED_APPS` in your Django settings to apply it
automatically.

See `proxyprefix.patch.patch_get_script_name` for details.

"""
from proxyprefix.patch import patch_get_script_name


patch_get_script_name()
