from urllib import urlencode
import httplib2

from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from facade.models import Mapping


def _fetch_target(request, target_url):
	http_client = httplib2.Http()
	
	if request.GET:
		target_url += '?' + urlencode(request.GET)
		
	response, content = http_client.request(target_url, method="GET")

	for mapping in Mapping.objects.all():
		replacement_url= request.build_absolute_uri(reverse('facade.views.bridge', args=(mapping.plug,)))
		content = content.replace(mapping.target_url, replacement_url)
	
	return http.HttpResponse(
		content,
		status=response.status
	)
	

@login_required
def bridge(request, target):

	try:
		mapping = Mapping.objects.get(plug=target)
	except Mapping.DoesNotExist:
		raise http.Http404
	
	return _fetch_target(request, mapping.target_url)
