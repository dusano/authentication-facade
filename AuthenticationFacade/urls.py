from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
admin.autodiscover()


if settings.GOOGLE_OAUTH:
	admin.site.login = login_required(admin.site.login)

urlpatterns = patterns('',
    
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'dashboard.views.index'),
	
	url(r'^accounts/login/$', 'gauth.views.login_page', name='gauth.login'),
	url(r'^accounts/google_callback/$', 'gauth.views.google_callback', name='gauth.google_callback'),

	url(r'^', include('facade.urls')),

)
