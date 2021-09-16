import os
# Google OAuth 2.0 Client configuration https://console.cloud.google.com/apis/credentials
#  callback_url should be set to the authorized redirect URI based on where server is
#  started
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
callback_url = os.environ['CALLBACK_URL']

# Faucet address and private key
faucet_address = os.environ['FAUCET_ADDRESS']
faucet_key = os.environ['FAUCET_KEY']

# Ropsten configuration
node_url = os.environ['NODE_URL']
