import os
from contract import fContract
from chain import handle_event, web3, Web3
from model import get_pinata_object
from flow_py_sdk import flow_client, AccountKey, signer, ProposalKey, cadence, Tx
import asyncio
from flow_py_sdk.signer import InMemorySigner, HashAlgo, SignAlgo
import subprocess

def register_on_contract(cost):
    
    pinata = get_pinata_object()
    image_ipfs = pinata.pin_file_to_ipfs("node.png")
    file_ipfs = pinata.pin_file_to_ipfs("model.py")
    
    metadata_json = {
        "name": "Flow AI Node",
        "description": "Decentralized AI inference nodes",
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
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                register_responder(metadata_ipfs["IpfsHash"], image_ipfs["IpfsHash"])))
    finally:
        loop.close() 


async def register_responder(
    url: str,
    img: str
):
    async with flow_client(
            host="access.devnet.nodes.onflow.org", port=9000
        ) as client:
        
        cmd = f'flow transactions send cadence/transactions/register_responder.cdc 1 "{url}" "Flow AI Node" "Decentralized AI inference nodes" "{img}" --network=testnet --signer=testnet-account'
        print(cmd)
        arch = subprocess.check_output(cmd, shell=True)
        print(arch)
        