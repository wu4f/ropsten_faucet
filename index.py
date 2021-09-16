from flask import render_template, session
from requests_oauthlib import OAuth2Session
from flask.views import MethodView
import model
import config

class Index(MethodView):
    def get(self):
        if ('oauth_token' in session):
            google = OAuth2Session(config.client_id, token=session['oauth_token'])
            userinfo = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
            email = userinfo['email']
            return render_template('index.html', email=email)
        else:
            return render_template('index.html')
