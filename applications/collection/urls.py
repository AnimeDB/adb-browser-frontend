from django.conf.urls.defaults import *

urlpatterns = patterns('applications.collection.views',
    url(r'^$', 'browse', name='collection_browse'),
    url(r'^(?P<model>(movies|genres|actors))/(?P<letter>([a-z]|09|@!))/$', 'browse', name='collection_browse_letter'),
)
