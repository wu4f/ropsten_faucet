from web3 import Web3
from flask import redirect, request, url_for, render_template, session
from flask.views import MethodView
import config
import time

class Index(MethodView):
    def get(self):
        return render_template('index.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        if (Web3.isAddress(request.form['address'])):
            w3 = Web3(Web3.HTTPProvider(config.node_url))
            from_address = Web3.toChecksumAddress(config.faucet_address)
            to_address = Web3.toChecksumAddress(request.form['address'])
            to_balance = w3.eth.get_balance(to_address)
            if to_balance < 10000000000000000000:
                nonce = w3.eth.getTransactionCount(from_address)
                gasPrice = w3.toWei(40.0, 'gwei')
                tx = {
                        'nonce': nonce,
                        'to': to_address,
                        'value': w3.toWei(10.00, 'ether'),
                        'gas': 21000,
                        'gasPrice': gasPrice
                }
                signed_tx = w3.eth.account.signTransaction(tx, config.faucet_key)
                tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction).hex()
                return render_template('index.html', tx_hash=tx_hash)
            else:
                return render_template('index.html', wait=1)
        else:
            return render_template('index.html')

