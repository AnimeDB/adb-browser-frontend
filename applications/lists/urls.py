from django.conf.urls.defaults import *

urlpatterns = patterns('applications.lists.views',
    url(r'^create.html$', 'edit', name='create'),
    url(r'^(?P<id>\d+)/$', 'view', name='view'),
    url(r'^(?P<id>\d+)/delete/$', 'delete', name='delete'),
    url(r'^(?P<id>\d+)/rename/$', 'edit', name='rename'),
)
