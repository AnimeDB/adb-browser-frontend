from django.conf.urls.defaults import *

urlpatterns = patterns('adb.frontend.collection.views',
    url(r'^$', 'browse', name='browse'),
    url(r'^(?P<model>(movies|genres|actors))/(?P<letter>([a-z]|09|@!))/$', 'browse', name='browse_per_letter'),
    url(r'^movie/(\d+)/$', 'movie', name='movie'),
    url(r'^genre/(\d+)/$', 'genre', name='genre'),
    url(r'^actor/(\d+)/$', 'actor', name='actor'),
)
