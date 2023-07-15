import os
from contract import fContract
from chain import handle_event, web3, Web3
from model import get_pinata_object
from flow_py_sdk import flow_client, AccountKey, signer


def register_on_contract(cost):
    
    # Get account
    web3.eth.account.enable_unaudited_hdwallet_features()
    mnemonic = ""
    with open('mnemonic.txt') as f:
        lines = f.readlines()
        mnemonic = lines[0]
    account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/539'/0'/0/0")
    
    account1, signer1 = AccountKey.from_seed(
            sign_algo=signer.SignAlgo.ECDSA_P256,
            hash_algo=signer.HashAlgo.SHA3_256,
            seed=mnemonic,
        )
    
    
    
    pinata = get_pinata_object()
    image_ipfs = pinata.pin_file_to_ipfs("node.png")
    file_ipfs = pinata.pin_file_to_ipfs("model.py")
    metadata_json = {
        "name": "Decent AI Node",
        "description": "Created by " + account.address,
        "image": image_ipfs["IpfsHash"],
        "attributes": [
            {
                "trait_type": "Model",
                "value": "runwayml/stable-diffusion-v1-5"
            },
            {
                "trait_type": "Model file",
                "value": file_ipfs["IpfsHash"]
            }
        ]
    }
    
    metadata_ipfs = pinata.pin_json_to_ipfs(metadata_json)
    
    # Send call to register on contract
    chain_id = web3.eth.chain_id
    tx = fContract.functions.registerResponder(cost, metadata_ipfs["IpfsHash"]).buildTransaction({
        "chainId": chain_id,
        'nonce': web3.eth.getTransactionCount(account.address),
        'from': account.address
    })
    print(tx)
    signed_tx = web3.eth.account.signTransaction(tx, private_key=account.key)

    sentTx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    
    # Send call to fetch all past events from contract with 0x in responder field
    event_filter = fContract.events.RequestRecieved.createFilter(fromBlock=1401055, argument_filters={'responder':"0x0000000000000000000000000000000000000000"})
    
    # Select random 10 and send to model_runner
    count = 0
    for PairCreated in event_filter.get_all_entries():
        print("Sending to model_runner")
        handle_event(PairCreated)
        count += 1
        if count == 10:
            break
