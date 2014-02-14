from django.conf.urls import url, patterns

urlpatterns = patterns('facade.views',

	url(r'b/(.+)', 'bridge', name='facade.bridge'),
	
)