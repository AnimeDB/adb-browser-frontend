from django.conf.urls.defaults import *

urlpatterns = patterns('collection.views',
    url(r'^$', 'browse', name='collection_browse'),
    url(r'^(?P<letter>([a-z]|0-9|@!))/$', 'browse', name='collection_browse_letter'),
)
