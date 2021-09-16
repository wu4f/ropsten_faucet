from flask import redirect, request, url_for, session
from requests_oauthlib import OAuth2Session
from flask.views import MethodView
import config

class Callback(MethodView):
    def get(self):
        google = OAuth2Session(config.client_id, redirect_uri = config.callback_url, state=session['oauth_state'])
        token = google.fetch_token(config.token_url, client_secret=config.client_secret,
                            authorization_response=request.url)
        # At this point you can fetch protected resources but lets save
        # the token and show how this is done from a persisted token
        session['oauth_token'] = token

        return redirect(url_for('eth'))
