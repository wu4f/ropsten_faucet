# ropsten_faucet
## A faucet for the Ropsten Ethereum testnet written in Python.

- Uses OAuth 2.0 to limit faucet requests to one per e-mail address per day
- Limits issuances to wallets with < 10 ETH in them
- Configuration done via environment variables in config.py
