from django.conf.urls.defaults import *

urlpatterns = patterns('applications.checker.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<release>\d+)/$', 'check', name='check'),
)
