####

import gdata.photos.service
import gdata.media
import gdata.geo


import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

from datetime import datetime
from datetime import timedelta

from apiclient.discovery import build



def GoogleAuthenticate(client_secrets, credential_store, scopeRequired):
	authStorage=Storage(credential_store)
	cachedAuthorisation=authStorage.get()
   	if cachedAuthorisation is None or cachedAuthorisation.invalid:
		flow = client.flow_from_clientsecrets(client_secrets,
#			scope='https://www.googleapis.com/auth/photos https://www.googleapis.com/auth/userinfo.profile',
			scopeRequired,
			redirect_uri='urn:ietf:wg:oauth:2.0:oob')
		auth_uri = flow.step1_get_authorize_url()
		print "Please visit the following URL and authenticate:"
		print
		print ShortenUrl(auth_uri)
		print
		auth_code = raw_input('Enter the auth code: ')
		cachedAuthorisation = flow.step2_exchange(auth_code)

	if (cachedAuthorisation.token_expiry - datetime.utcnow()) < timedelta(minutes=5):
		http = cachedAuthorisation.authorize(httplib2.Http())
		cachedAuthorisation.refresh(http)

	authStorage.put(cachedAuthorisation)

	return cachedAuthorisation.access_token


def GetPhotoService(access_token):
	user_agent='bjfapp'
	gd_client = gdata.photos.service.PhotosService(source=user_agent,
		email="default",
		additional_headers={'Authorization' : 'Bearer %s' % access_token})
	return gd_client



def ShortenUrl(longUrl):
	service=build('urlshortener', 'v1', developerKey="AIzaSyByfFrUjRfa-aAxqidlczHdRuj7IX4V0lQ")
	url=service.url()
	body={'longUrl':longUrl}
	resp=url.insert(body=body).execute()
	return resp['id']


