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
        users = [ dict(name=row[0], ip=row[1], wallet=row[2], last=datetime.fromtimestamp(row[3]).astimezone(timezone(timedelta(hours=-8))).strftime('%m-%d %H:%M')) for row in m.select_all(sort) if row[3] < now]
        return render_template('users.html',users=users)

