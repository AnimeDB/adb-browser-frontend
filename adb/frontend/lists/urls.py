from django.conf.urls.defaults import *

urlpatterns = patterns('adb.frontend.lists.views',
    url(r'^$', 'index', name='index'),
    url(r'^create/$', 'edit', name='create'),
    url(r'^(?P<id>\d+)/$', 'view', name='view'),
    url(r'^(?P<id>\d+)/delete/$', 'delete', name='delete'),
    url(r'^(?P<id>\d+)/rename/$', 'edit', name='rename'),
)
