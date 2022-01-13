from web3 import Web3
from flask import redirect, request, url_for, render_template, session
from flask.views import MethodView
import model
from datetime import datetime

class Users(MethodView):
    def get(self):
        m = model.get_model()
        users = [ dict(name=row[0], ip=row[1], wallet=row[2], last=datetime.fromtimestamp(row[3]).strftime('%m-%d %H:%M')) for row in m.select_all() ]
        return render_template('users.html',users=users)
