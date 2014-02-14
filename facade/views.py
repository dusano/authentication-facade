from django import http
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def bridge(request, target):
	return http.HttpResponse("<html><body>Target: %s</body></html>" % target)
