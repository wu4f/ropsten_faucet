from web3 import Web3
from flask import redirect, request, url_for, render_template, session
from requests_oauthlib import OAuth2Session
from flask.views import MethodView
import model
import config
import time

class Eth(MethodView):
    def get(self):
        # If client has an OAuth2 token, use it to get their information and render
        #   the eth page with it
        if 'oauth_token' in session:
            google = OAuth2Session(config.client_id, token=session['oauth_token'])
            try:
                userinfo = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
            except:
                return redirect(url_for('logout'))

            email = userinfo['email']
            m = model.get_model()
            wait_time = int(time.time()) - m.select(email)
            if wait_time < 86400:
                return render_template('eth.html', email=userinfo['email'], wait=wait_time)
            else:
                return render_template('eth.html', email=userinfo['email'])
        else:
        # Redirect to the identity provider and ask the identity provider to return the client
        #   back to /callback route with the code
            google = OAuth2Session(config.client_id,
                    redirect_uri = config.callback_url,
                    scope = 'https://www.googleapis.com/auth/userinfo.email'
            )
            authorization_url, state = google.authorization_url(config.authorization_base_url)

            # Identity provider returns URL and random "state" that must be echoed later
            #   to prevent CSRF.
            session['oauth_state'] = state
            return redirect(authorization_url)

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        def send_eth(to_address):
            w3 = Web3(Web3.HTTPProvider(config.node_url))
            address1 = Web3.toChecksumAddress(config.faucet_address)
            address2 = Web3.toChecksumAddress(to_address)
            to_balance = w3.eth.get_balance(address2)
            if to_balance > 10000000000000000000:
                return 0
            nonce = w3.eth.getTransactionCount(address1)
            tx = {
                    'nonce': nonce,
                    'to': address2,
                    'value': w3.toWei(10.00, 'ether'),
                    'gas': 21000,
                    'maxFeePerGas': w3.toWei(5.0, 'gwei'),
                    'maxPriorityFeePerGas': w3.toWei(5.0, 'gwei'),
                    'chainId': 3,
            }
            signed_tx = w3.eth.account.signTransaction(tx, config.faucet_key)
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction).hex()
            return tx_hash

        if ('oauth_token' in session) and ('address' in request.form) and Web3.isAddress(request.form['address']):
            # Insert based on form fields only if an OAuth2 token is present to ensure
            #   values in all fields exist
            google = OAuth2Session(config.client_id, token=session['oauth_token'])
            try:
                userinfo = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
            except:
                return redirect(url_for('logout'))

            email = userinfo['email']
            if request.headers.getlist("X-Forwarded-For"):
                ip = request.headers.getlist("X-Forwarded-For")[0]
            else:
                ip = request.remote_addr
            wallet = request.form['address']
            m = model.get_model()
            last = m.select(email)
            if last == 0:
                m.insert(email, ip, wallet)
                tx_hash = send_eth(wallet)
                return render_template('eth.html', email=userinfo['email'], tx_hash=tx_hash, wait=1)
            elif int(time.time()) - last > 604800:
                m.update(email, ip, wallet)
                tx_hash = send_eth(wallet)
                return render_template('eth.html', email=userinfo['email'], tx_hash=tx_hash, wait=1)
            else:
                return redirect(url_for('eth'))
        else:
            return redirect(url_for('eth'))
