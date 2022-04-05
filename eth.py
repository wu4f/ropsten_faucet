from web3 import Web3
from flask import redirect, request, url_for, render_template, session
from requests_oauthlib import OAuth2Session
from flask.views import MethodView
import model
import config
import time
import logging
from datetime import datetime, timezone, timedelta

class Eth(MethodView):
    def validate_oauth(self, session):
        google = OAuth2Session(config.client_id, token=session['oauth_token'])
        try:
            userinfo = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
            email = userinfo['email']
        except:
            return ""
        return email

    def validate_ip(self, request):
        if request.headers.getlist("X-Forwarded-For"):
            return request.headers.getlist("X-Forwarded-For")[0]
        else:
            return request.remote_addr

    def validate_wallet(self, request):
        if ('address' in request.form) and Web3.isAddress(request.form['address']):
            return request.form['address']
        return ""
    
    def calculate_eth(self, email, ip, wallet, last):
        now = datetime.now().astimezone(timezone(timedelta(hours=-7))).strftime('%m-%d %H:%M')
        delta = int(time.time()) - last
        if delta < 1209600:
            now = datetime.now().astimezone(timezone(timedelta(hours=-7))).strftime('%m-%d %H:%M')
            logging.info(f'{now}:Rate Limit:{email}:{ip}:{wallet}:{delta}')
            return 0.0

        if email.endswith('@pdx.edu'):
            logging.info(f'{now}:Eth Max:{email}:{ip}:{wallet}')
            return 10.0
        
        m = model.get_model()
        last_ips = m.select_last_ip(5)
        if any([ip.startswith(substring) for substring in last_ips]):
            logging.info(f'{now}:Eth Blocked Last:{email}:{ip}:{wallet}') 
            return 0.0

        return 5.0

    def send_eth(self, email, ip, to_address, send_amount):
        w3 = Web3(Web3.HTTPProvider(config.node_url))
        address1 = Web3.toChecksumAddress(config.faucet_address)
        address2 = Web3.toChecksumAddress(to_address)
        to_balance = w3.eth.get_balance(address2)
        if to_balance > 5000000000000000000:
            now = datetime.now().astimezone(timezone(timedelta(hours=-7))).strftime('%m-%d %H:%M')
            logging.info(f'{now}:High Balance:{email}:{ip}:{to_address}')
            return 0
        nonce = w3.eth.getTransactionCount(address1)
        tx = {
                'nonce': nonce,
                'to': address2,
                'value': w3.toWei(send_amount, 'ether'),
                'gas': 21000,
                'maxFeePerGas': w3.toWei(1000.0, 'gwei'),
                'maxPriorityFeePerGas': w3.toWei(500.0, 'gwei'),
                'chainId': 3,
        }
        now = datetime.now().astimezone(timezone(timedelta(hours=-7))).strftime('%m-%d %H:%M')
        logging.info(f'{now}:Transaction attempt:{email}:{ip}:{to_address}')
        signed_tx = w3.eth.account.signTransaction(tx, config.faucet_key)
        try:
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction).hex()
        except:
            logging.exception(f'{now}:Failed Transaction:{email}:{ip}:{to_address}')
            return 0
        return tx_hash

    def get(self):
        if not 'oauth_token' in session:
        # Redirect to the identity provider if no token.
        # Provider returns client to callback_url after auth
            google = OAuth2Session(config.client_id,
                    redirect_uri = config.callback_url,
                    scope = 'https://www.googleapis.com/auth/userinfo.email'
            )
            authorization_url, state = google.authorization_url(config.authorization_base_url)

            # Identity provider returns URL and random "state" to echo
            # to prevent CSRF.
            session['oauth_state'] = state
            return redirect(authorization_url)

        email = self.validate_oauth(session)
        ip = self.validate_ip(request)

        if (not email) or (not ip):
            return redirect(url_for('logout'))

        m = model.get_model()
        wait_time = int(time.time()) - m.select(email, ip, "y")
        if wait_time < 1209600:
            return render_template('eth.html', email=email, wait=1)
        else:
            return render_template('eth.html', email=email)

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        if not 'oauth_token' in session:
            return redirect(url_for('eth'))

        email = self.validate_oauth(session)
        ip = self.validate_ip(request)

        if (not email) or (not ip):
            return redirect(url_for('logout'))

        wallet = self.validate_wallet(request)
        if not wallet:
            return redirect(url_for('eth'))

        m = model.get_model()
        last = m.select(email,ip,wallet)

        send_amount = self.calculate_eth(email, ip, wallet, last)

        tx_hash = 0
        if send_amount > 0:
            tx_hash = self.send_eth(email, ip, wallet, send_amount)

        if tx_hash:
            if last == 0:
                m.insert(email, ip, wallet, send_amount)
            else:
                m.update(email, ip, wallet, send_amount)

        return render_template('eth.html', email=email, tx_hash=tx_hash, wait=1)
