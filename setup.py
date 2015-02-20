from setuptools import setup

import proxyprefix


setup(
    name='proxyprefix',
    version=proxyprefix.__version__,
    description='Prefix SCRIPT_NAME with X-Forwarded-Prefix header',
    long_description=proxyprefix.__doc__,
    url='https://github.com/yola/proxyprefix',
    packages=['proxyprefix'],
    test_suite='nose.collector',
)
