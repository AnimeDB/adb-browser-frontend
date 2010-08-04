from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^collection/', include('applications.collection.urls', namespace='collection')),
    url(r'^lists/', include('applications.lists.urls', namespace='lists')),
    
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}, name='index'),
    url(r'^login.html$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout.html$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s(?P<path>.*)$' % (settings.MEDIA_URL[1:]), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
