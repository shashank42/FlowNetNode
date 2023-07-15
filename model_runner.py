import json
import asyncio
from model import infer
import subprocess

def run_model(prompt, request_id):
    
    fname = infer(prompt, request_id)    
    print("Got back inference, now make call to contract")
    
    cmd = f'flow transactions send cadence/transactions/submit_inference.cdc {request_id} "{url}" --network=testnet --signer=testnet-account'
    print(cmd)
    arch = subprocess.check_output(cmd, shell=True)
    print(arch)
