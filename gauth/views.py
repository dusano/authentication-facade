import urllib

from django.conf import settings
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import django.contrib.auth as auth

from backend import get_oauth_url, authorize


def login_page(request):
	if not settings.GOOGLE_OAUTH:
		return redirect('admin:index')

	oauth_error = request.GET.get('oauth_error', '')
	oauth_url = get_oauth_url(request)

	next_path = request.GET.get('next', '')
	request.session['login_next'] = next_path

	return render_to_response('login.html', {
		'error': oauth_error,
		'oauth_url': oauth_url,
	})

def google_callback(request):
	next_path = request.session.get('login_next')

	user_data = authorize(request)
	if not user_data:
		return _fail_response(next_path=next_path)
	if not user_data['verified_email']:
		return _fail_response(next_path=next_path)

	user = auth.authenticate(oauth_data=user_data)

	if not user or not user.is_active:
		return _fail_response('Your Google account is not connected with Authentication Facade.')

	auth.login(request, user)

	if not next_path:
		return redirect('admin:index')

	return redirect(next_path)


def _fail_response(message='Google authentication failed.', next_path=None):
	url = reverse(login_page)

	attrs = {}
	if message:
		attrs['oauth_error'] = message
	if next_path:
		attrs['next'] = next_path

	url +=  "?" + urllib.urlencode(attrs)

	return redirect(url)
