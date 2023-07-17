import os
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
                register_responder(metadata_ipfs["IpfsHash"], image_ipfs["IpfsHash"], cost)))
    finally:
        loop.close() 


async def register_responder(
    url: str,
    img: str,
    cost: int
):
    
    cmd = f'flow transactions send cadence/transactions/setup_account.cdc --network=testnet --signer=testnet-account'
    print(cmd)
    arch = subprocess.check_output(cmd, shell=True)
    print(arch)

    cmd = f'flow transactions send cadence/transactions/register_responder.cdc {cost} "{url}" "FlowNet AI Node" "Decentralized AI inference nodes utilizing the Flow Blockchain" "{img}" --network=testnet --signer=testnet-account'
    print(cmd)
    arch = subprocess.check_output(cmd, shell=True)
    print(arch)
    
    
        