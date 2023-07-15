import click
import pyperclip
import os
from chain import main_loop
from register import register_on_contract
from flow_py_sdk import flow_client, AccountKey, signer, Script
import asyncio
import json
from model import infer


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@click.option('-l', '--length', type=int, help='Length of password to be generated')
@click.option('-o', '--option', type=click.Choice(['1', '2', '3', '4']), default = '4',
    help='''Options\n
    1 - alphabetic lowercase\n
    2 - alphabetic both cases\n
    3 - alphanumeric\n
    4 - alphanumeric + special characters'''
)
def generate(length, option):
    click.echo(length)
    click.echo(option)
    """generates a random password of length and type"""
    logo = """
    +-----------------------------+
    | Thank you for using Ranpass |
    +-----------------------------+
    """
    # generate random password
    password = "cool" # application.generate(int(length), int(option))

    # copy password to clipboard
    try:
        pyperclip.copy(password)
        click.echo('Password has been copied to clipboard\n')
    except Exception:
        click.echo('Could not copy password to clipboad\n')

    # output password and info to terminal
    click.echo(password)
    click.echo(logo)
    

@cli.command()
@click.option("-i", "--info", is_flag=True, show_default=True, default=False, help="Get wallet associated to the node.")
# @click.option("-c", "--create", is_flag=True, show_default=True, default=False, help="Create a new wallet if it doesn't exist.")
@click.option("-s", "--save", prompt=True, prompt_required=False, help="Provide the address and key (private) to be stored for future operations. Comma separate them.")
def wallet(info, save):
    
    # only one of the the parameters can be true
    if (info + (save is not None)) > 1:
        click.echo("Only one of the parameters can be true")
        return
    
    if (info):
        flow_json = ""
        
        # ensure that mnemonic file exists
        if not (os.path.exists('flow.json')):
            click.echo("flow.json file doesn't exist. Please create a new wallet with flow-cli or save a wallet using -s")
            return
        
        with open('flow.json') as f:
            flow_json = json.load(f)
            lines = f.readlines()
            if "accounts" not in flow_json.keys():
                click.echo("No accounts found. Please create a new wallet with flow-cli or save a wallet using -s")
                return
            if "testnet-account" not in flow_json["accounts"].keys():
                click.echo("Testnet account not found in flow.json. Please create a new wallet with flow-cli or save a wallet using -s")
                return
        testnet_account = flow_json["accounts"]["testnet-account"]

        click.echo("Address on Flow : ") 
        click.echo(testnet_account["address"])
        
        click.echo("Private key : ") 
        click.echo(testnet_account["key"])
        
        return
        
    # Check if mnemonic file already exists, if it exists don't allow to replace
    if (os.path.exists('flow.json')):
        with open('flow.json', 'r') as f:
            flow_json = json.load(f)
            if "accounts" in flow_json and "testnet-account" in flow_json["accounts"]:
                click.echo("Secrets already exists. Please consider before replacing them.")
                return
            
    # if (create):
    #     # Not implemented
    #     pass
    
    if (save):
        address = save.split(",")[0]
        key = save.split(",")[1]

        with open('flow.json', 'r') as f:
            flow_json = json.load(f)
            flow_json["accounts"]["testnet-account"] = {
                "address": address,
                "key": key
            }
            # flow_json.dump("flow.json")
            json.dump(flow_json, open("flow.json","w"))
        click.echo("Flow address : ")
        click.echo(address) 
        click.echo("Key : ")
        click.echo(key)
        return

@cli.command()
@click.option('-k', '--key', help='API key provided by pinata')
@click.option('-s', '--secret', help='API secret provided by pinata')
def pinata(key, secret):
    
    # Save the api key and secret api key in a file
    with open('pinata.txt', 'w') as f:
        l1 = key+"\n"
        l2 = secret+"\n"
        f.writelines([l1, l2])
    return


# Add code to register/update the node on the Inference Manager contract
@cli.command()
@click.option('-c', '--cost', type=int, help='Register on Decent AI Contract as a node')
def register(cost):
    
    register_on_contract(cost)
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                try_script()))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close() 
    
    pass


@cli.command()
@click.option("-p", "--prompt", prompt=True, prompt_required=False, help="Provide a prompt to test stable diffusion on.")
def test(prompt):
    
    ipfs = infer(prompt, 1, strength=.75, num_inference_steps=70, guidance_scale=11, num_images_per_prompt=1)
    print(ipfs)
    
    pass

# Simulate mode to calculate possible revenue vs runtime
@cli.command()
def start():

    # This code should start to run when the user runs the command. 
    # It should check if the wallet exists.
    # Start to run the while true script
   
    # ## Main purpose of the Inference node
    # 1. Run a loop to fetch past events from the Inference Manager contract and get latest unfulfilled inference requests and request pramas
    # 2. Use the local GPU or remote GPU to create an inference output (.jpg in this case)
    # 3. Submit a transaction to the Inference Manager to get rewarded

    # ## Side goals
    # 1. Ensure model good-ness to not slide on reputation rank
    # 2. Ensure that the node is registered on the Inference Manager
    # 3. Do a simulation right before submitting the result to ensure that the transaction will be successful, if not discard the result and listen for next request
    
    main_loop()

    
    pass