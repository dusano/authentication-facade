import httplib2

from django import http
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from facade.models import Mapping


def _fetch_target(target_url):
	http_client = httplib2.Http()
	response, content = http_client.request(target_url, method="GET")
	
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
	
	return _fetch_target(mapping.target_url)
