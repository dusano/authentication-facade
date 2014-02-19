from urllib import urlencode
import httplib2

from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from facade.models import Mapping


HEADERS_TO_PASS = [
		'content-type',
	]

def _fetch_target(request, target_url):
	http_client = httplib2.Http(disable_ssl_certificate_validation=True)

	if request.GET:
		target_url += '?' + urlencode(request.GET)

	target_response, content = http_client.request(target_url, method="GET")

	if ('content-type' in target_response) and target_response['content-type'].startswith('text/html'):
		for mapping in Mapping.objects.all():
			replacement_url= request.build_absolute_uri(reverse('facade.views.bridge', args=(mapping.plug,)))
			content = content.replace(mapping.target_url, replacement_url)

	response = http.HttpResponse(
			content,
			status=target_response.status
		)

	for header in HEADERS_TO_PASS:
		if header in target_response:
			response[header] = target_response[header]

	return response


#@login_required
def bridge(request, target):

	try:
		mapping = Mapping.objects.get(plug=target)
	except Mapping.DoesNotExist:
		raise http.Http404

	return _fetch_target(request, mapping.target_url)
