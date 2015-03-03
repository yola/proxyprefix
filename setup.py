from setuptools import find_packages, setup

import proxyprefix


setup(
    name='proxyprefix',
    version=proxyprefix.__version__,
    description='Prefix SCRIPT_NAME with X-Forwarded-Prefix header',
    long_description=proxyprefix.__doc__,
    author='Yola',
    author_email='engineers@yola.com',
    license='MIT (Expat)',
    url='https://github.com/yola/proxyprefix',
    packages=find_packages(exclude=['tests', 'tests.*']),
    test_suite='nose.collector',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
    ],
    extras_require = {
        'djproxy': ['djproxy>=2.0.0'],
    },
)
