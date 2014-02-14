from django import http
from django.shortcuts import render

def bridge(request, target):
	return http.HttpResponse("<html><body>Target: %s</body></html>" % target)
