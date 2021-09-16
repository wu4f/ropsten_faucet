from flask import redirect, url_for, session
from flask.views import MethodView

class Logout(MethodView):
    def get(self):
        session.clear()
        return redirect(url_for('index'))