import httplib2
import logging
import json

from django.conf import settings

from django.core.urlresolvers import reverse
from oauth2client.client import OAuth2WebServerFlow
from django.contrib.auth import models, backends


URL_APP_TOKEN = "https://accounts.google.com/o/oauth2/auth"
URL_USERINFO = "https://www.googleapis.com/oauth2/v2/userinfo"

logger = logging.getLogger(__name__)

def get_flow(request):
	url = 'https://%s%s' % (request.get_host(), reverse('gauth.google_callback'))

	return OAuth2WebServerFlow(
			client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
			client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
			scope='email',
			access_type='online',
			redirect_uri=url
		)


def get_oauth_url(request):
	return get_flow(request).step1_get_authorize_url()


def authorize(request):
	try:
		code = request.GET.get('code')
		if not code:
			return None

		flow = get_flow(request)
		credentials = flow.step2_exchange(code)
		headers = httplib2.Http()
		credentials.authorize(headers)

		http = httplib2.Http()
		http = credentials.authorize(http)

		resp, content = http.request(URL_USERINFO, method="GET")

		if resp and resp.status == 200:
			return json.loads(content)

	except Exception:
		logger.error('Google authentification failed', exc_info=True)

	return None


class GoogleOauthBackend(backends.ModelBackend):
	def authenticate(self, oauth_data=None):
		try:
			user = models.User.objects.get(email=oauth_data['email'])
			if oauth_data and oauth_data['verified_email']:
				return user
			return None

		except models.User.DoesNotExist:
			return None
