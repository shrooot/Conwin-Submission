from django.shortcuts import render
from google_auth_oauthlib.flow import Flow
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as GoogleApiClientBuild
import os

GOOGLE_CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email',
                          'https://www.googleapis.com/auth/userinfo.profile',
                          'openid']


def get_google_calendar_flow():
    credentials_file = os.path.join(
        os.path.dirname(__file__), 'client_secret.json')
    return Flow.from_client_secrets_file(credentials_file, scopes=GOOGLE_CALENDAR_SCOPES, redirect_uri="http://127.0.0.1:8000/rest/v1/calendar/redirect")


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def GoogleCalendarInitView(request):
    flow = get_google_calendar_flow()
    flow.redirect_uri = "http://127.0.0.1:8000/rest/v1/calendar/redirect"

    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')

    request.session['google_calendar_oauth_state'] = state

    return HttpResponseRedirect(authorization_url)


def GoogleCalendarRedirectView(request):
    state = request.session.pop('google_calendar_oauth_state', None)
    flow = get_google_calendar_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    if 'credentials' not in request.session:
        return redirect('v1/calendar/init')

    credentials = Credentials(
        **request.session['credentials'])

    service = GoogleApiClientBuild("calendar", 'v3', credentials=credentials)

    calendar_list = service.calendarList().list().execute()

    calendar_id = calendar_list['items'][0]['id']
    events = service.events().list(calendarId=calendar_id).execute()
    events_list_append = []
    if not events['items']:
        print('No data found.')
        return HttpResponse("No data found or user credentials invalid.")
    else:
        for events_list in events['items']:
            events_list_append.append(events_list)
            return HttpResponse(str(events_list_append))
    return HttpResponse("calendar event aren't here")
