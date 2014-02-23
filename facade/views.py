import re
from urllib import urlencode
import urlparse
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
	
	parsed_target_url = list(urlparse.urlparse(target_url))
	
	basic_auth = re.match('^(.*):(.*)@(.*)$', parsed_target_url[1])
	
	if basic_auth and basic_auth.groups:
		http_client.add_credentials(basic_auth.group(1), basic_auth.group(2))
		parsed_target_url[1] = basic_auth.group(3)
	
	if request.GET:
		if parsed_target_url[4]:
			parsed_target_url[4] += '&'
		
		parsed_target_url[4] += urlencode(request.GET)
		
	fetch_url = urlparse.urlunparse(parsed_target_url)
	
	target_response, content = http_client.request(fetch_url, method="GET")

	if ('content-type' in target_response) and target_response['content-type'].startswith('text/html'):
		for mapping in Mapping.objects.all():
			replacement_url= request.build_absolute_uri(reverse('facade.views.bridge', args=(mapping.plug,)))
			content = content.replace(mapping.target_url, replacement_url)
			if mapping.pattern:
				content = content.replace(mapping.pattern, replacement_url)

	response = http.HttpResponse(
			content,
			status=target_response.status
		)

	for header in HEADERS_TO_PASS:
		if header in target_response:
			response[header] = target_response[header]

	return response


@login_required
def bridge(request, target):

	try:
		mapping = Mapping.objects.get(plug=target)
	except Mapping.DoesNotExist:
		raise http.Http404

	return _fetch_target(request, mapping.target_url)
