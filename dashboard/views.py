from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from facade.models import Mapping


#@login_required
def index(request):

	mappings = Mapping.objects.filter(index_page=True)

	groups_and_mappings = {}
	for mapping in mappings:
		if mapping.group not in groups_and_mappings:
			groups_and_mappings[mapping.group] = []

		groups_and_mappings[mapping.group].append(mapping)

	return render_to_response('index.html',
			{'groups_and_mappings' : groups_and_mappings},
			context_instance=RequestContext(request)
		)
