
from web3 import Web3
import json
# from web3.providers.rpc import HTTPProvider
# from web3.middleware import geth_poa_middleware
import asyncio
from model_runner import run_model
from contract import fContract, web3


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


# define function to handle events and print to the console
def handle_event(event):
    print(Web3.toJSON(event))
    request = Web3.toJSON(event)
    request = eval(request)
    run_model(request["args"]["prompt"], request["args"]["requestId"])
    

    
    
    # Create a submit inference transaction
    # and send to tenderly to simulate if success, if success then send to the blockchain
    # else just log as would have failed and credit tenderly the amount saved
    
    # Sample output
    # {
    #     "args": {
    #         "requestor": "0x8A0B9D49252825211b512b719258507Fa3Fda69E",
    #         "responder": "0x8A0B9D49252825211b512b719258507Fa3Fda69E",
    #         "requestId": 2,
    #         "prompt": "People skiing in denver snow",
    #         "offer": 0
    #     },
    #     "event": "RequestRecieved",
    #     "logIndex": 199,
    #     "transactionIndex": 47,
    #     "transactionHash": "0x0adcb2ed50a043ff309791cd164e54853bed11485b589dff2c1045f0aca1bea2",
    #     "address": "0x7C14dd39c29a22E69b99E41f7A3E607bfb63d244",
    #     "blockHash": "0x9713b2773eb37ccab7aa9f6cce9f14f5cca47a1673a6c67e08c2fa8b8314ae1d",
    #     "blockNumber": 39896349
    # }
    

    


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main_loop():
    
    # Get account
    web3.eth.account.enable_unaudited_hdwallet_features()
    mnemonic = ""
    with open('mnemonic.txt') as f:
        lines = f.readlines()
        mnemonic = lines[0]
    account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/539'/0'/0/0")
    
    event_filter = fContract.events.RequestRecieved.createFilter(fromBlock='latest', argument_filters={'responder': account.address}) # , argument_filters={'responder': account.address}
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()

