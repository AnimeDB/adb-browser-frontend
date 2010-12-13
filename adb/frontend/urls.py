from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^collection/', include('adb.frontend.collection.urls', namespace='collection')),
    url(r'^lists/', include('adb.frontend.lists.urls', namespace='lists')),
    
    url(r'^checker/', include('adb.frontend.checker.urls', namespace='checker')),
    
    url(r'^search/', include('haystack.urls')),
    
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}, name='index'),
    url(r'^login.html$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout.html$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)


