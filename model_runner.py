

import json
# from web3.providers.rpc import HTTPProvider
# from web3.middleware import geth_poa_middleware
import asyncio
from model import infer
from contract import fContract, web3, Web3

# from web3 import Web3
# from web3.providers.rpc import HTTPProvider
# from web3.middleware import geth_poa_middleware

# PROVIDER = "wss://polygon-mainnet.g.alchemy.com/v2/_tn9X7pFnXwYXYi8Q33gQjRg_B3Dey_4"
# web3 = Web3(Web3.WebsocketProvider(PROVIDER))
# web3.middleware_onion.inject(geth_poa_middleware, layer=0)


# contractAddress = '0x7C14dd39c29a22E69b99E41f7A3E607bfb63d244'
# address2 = Web3.toChecksumAddress(contractAddress)

# PROVIDER = "wss://polygon-mainnet.g.alchemy.com/v2/_tn9X7pFnXwYXYi8Q33gQjRg_B3Dey_4"
# web3 = Web3(Web3.WebsocketProvider(PROVIDER))
# web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# import json
# abi = 1
# with open("./artifacts/InferenceManager.json", "r") as f:
#     abi = json.load(f)
#     abi = abi["abi"]

# fContract = web3.eth.contract(abi=abi,address=address2)


def run_model(prompt, request_id):
    
    fname = infer(prompt, request_id)
    
    print("Got back infernence, now make call to contract")

    # Get account
    mnemonic = ""
    with open('mnemonic.txt') as f:
        lines = f.readlines()
        mnemonic = lines[0]
        
    web3.eth.account.enable_unaudited_hdwallet_features()
    account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/539'/0'/0/0")

    chain_id = web3.eth.chain_id
    tx = fContract.functions.recieveInference(request_id, fname).buildTransaction({
        "chainId": chain_id,
        'nonce': web3.eth.getTransactionCount(account.address),
        'from': account.address
    })
    print(tx)
    signed_tx = web3.eth.account.signTransaction(tx, private_key=account.key)

    sentTx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

