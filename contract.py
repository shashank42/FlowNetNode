
from web3 import Web3
import json
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware
import asyncio

# Matic
# contractAddress = '0xe9AbD1263b5D024d6FC53fa1F98A4560615761B0'
# PROVIDER = "wss://polygon-mainnet.g.alchemy.com/v2/_tn9X7pFnXwYXYi8Q33gQjRg_B3Dey_4"
# web3 = Web3(Web3.WebsocketProvider(PROVIDER))

# Coinbase
contractAddress = '0x9d5CD448332A857F6BfDb7541CFc33C61789BB41' # <- bug in safeMint (onlyOwner)
# contractAddress = '0x5755f4B547596c4cc45AA898e076cd75EA10f374'
PROVIDER = "https://goerli.base.org"
web3 = Web3(Web3.HTTPProvider(PROVIDER))

address2 = Web3.to_checksum_address(contractAddress)
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

import json
abi = 1
with open("./artifacts/InferenceManager.json", "r") as f:
    abi = json.load(f)
    abi = abi["abi"]

fContract = web3.eth.contract(abi=abi,address=address2)
