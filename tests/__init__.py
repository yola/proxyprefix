import os

from django.conf import settings


# Configure django so that our tests work correctly
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.fake_app.settings'
settings._setup()
