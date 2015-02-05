from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^path/$', 'tests.fake_app.views.show_path', name='show_path'),
)
