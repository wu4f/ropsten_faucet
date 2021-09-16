"""
A simple guestbook flask app.
"""
import flask
import os
from index import Index

app = flask.Flask(__name__)       # our Flask app
app.secret_key = os.urandom(24)

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET","POST"])

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=8000, debug=True)
