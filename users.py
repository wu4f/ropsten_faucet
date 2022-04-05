from web3 import Web3
from flask import redirect, request, url_for, render_template, session
from flask.views import MethodView
import model
from datetime import datetime, timezone, timedelta
import time

class Users(MethodView):
    def get(self):
        m = model.get_model()
        now = int(time.time())
        sort = request.args.get('sort')
        users = [ dict(name=row[0], ip=row[1], wallet=row[2], last=datetime.fromtimestamp(row[3]).astimezone(timezone(timedelta(hours=-7))).strftime('%m-%d %H:%M'), eth=row[4]) for row in m.select_all(sort) ]
        return render_template('users.html',users=users)

