import click
import pyperclip
# from app import application
from web3 import Web3
import os
from chain import main_loop
from register import register_on_contract
from flow_py_sdk import flow_client, AccountKey, signer
from eth_account.hdaccount import (
    ETHEREUM_DEFAULT_PATH,
    generate_mnemonic,
    key_from_seed,
    seed_from_mnemonic,
)
from hexbytes import (
    HexBytes,
)


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
@click.option("-c", "--create", is_flag=True, show_default=True, default=False, help="Create a new wallet if it doesn't exist.")
@click.option("-s", "--save", prompt=True, prompt_required=False, help="Save user's provided seed phrase and treat that as the wallet.")
def wallet(info, create, save):
    
    # only one of the the parameters can be true
    if (info + create + (save is not None)) > 1:
        click.echo("Only one of the parameters can be true")
        return
    
    if (info):
        web3 = Web3()
        web3.eth.account.enable_unaudited_hdwallet_features()
        mnemonic = ""
        
        # ensure that mnemonic file exists
        if (not (os.path.exists('mnemonic.txt'))):
            click.echo("Mnemonic file doesn't exist. Please create a new wallet using the -c flag or save a wallet using -s")
            return
        
        with open('mnemonic.txt') as f:
            lines = f.readlines()
            if (len(lines) == 0):
                click.echo("No wallet found. Please create a new wallet using the -c flag or save a wallet using -s")
                return
            if (len(lines) > 1):
                click.echo("More than one line found in mnemonic.txt. Please delete the extra lines and try again.")
                return
            mnemonic = lines[0]
            # mnemonic must have 12 words
            if (len(mnemonic.split(" ")) != 12):
                click.echo("Invalid mnemonic. Mnemonic must have 12 words.")
                return
            
        account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/539'/0'/0/0")
        account1, signer1 = AccountKey.from_seed(
            sign_algo=signer.SignAlgo.ECDSA_P256,
            hash_algo=signer.HashAlgo.SHA3_256,
            seed=mnemonic,
        )
        click.echo(account.address)
        click.echo("Address Flow: ") 
        click.echo(account1)
        click.echo("Signer Flow: ")
        click.echo(signer1)
        return
        
    # Check if mnemonic file already exists, if it exists don't allow to replace
    if (os.path.exists('mnemonic.txt')):
        with open('mnemonic.txt', 'r') as f:
            lines = f.readlines()
            if (len(lines) > 0):
                click.echo("Mnemonic file already exists. Please consider before replacing the mnemonic.")
                return
    
    if (create):
        web3 = Web3()
        web3.eth.account.enable_unaudited_hdwallet_features()
        account, mnemonic = web3.eth.account.create_with_mnemonic()
        account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/539'/0'/0/0")
        account1, signer1 = AccountKey.from_seed(
            sign_algo=signer.SignAlgo.ECDSA_P256,
            hash_algo=signer.HashAlgo.SHA3_256,
            seed=mnemonic,
        )
        click.echo("Address: " + account.address)
        click.echo("Mnemonic: " + mnemonic)
        click.echo("Address Flow: ") 
        click.echo(account1)
        click.echo("Signer Flow: ")
        click.echo(signer1)
        
        click.echo("Please save this mnemonic in a safe place. This will be used to recover your wallet in the future.")
        with open('mnemonic.txt', 'w') as f:
            f.write(mnemonic)
        return
    
    if (save):
        web3 = Web3()
        web3.eth.account.enable_unaudited_hdwallet_features()
        mnemonic = save
        # mnemonic must have 12 words
        if (len(mnemonic.split(" ")) != 12):
            click.echo("Invalid mnemonic. Mnemonic must have 12 words.")
            return
        account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/539'/0'/0/0")
        account1, signer1 = AccountKey.from_seed(
            sign_algo=signer.SignAlgo.ECDSA_P256,
            hash_algo=signer.HashAlgo.SHA3_256,
            seed=mnemonic,
        )
        
        click.echo("Address: " + account.address)
        click.echo("Mnemonic: " + mnemonic)
        click.echo("Address Flow: ") 
        click.echo(account1)
        click.echo("Signer Flow: ")
        click.echo(signer1)
        click.echo("Please save this mnemonic in a safe place. This will be used to recover your wallet in the future.")
        with open('mnemonic.txt', 'w') as f:
            f.write(mnemonic)
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
async def register(cost):
    
    # register_on_contract(cost)
    
    
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port

    # --------------------------------
    # script without arguments Example
    # --------------------------------
    script = Script(
        code="""
                pub fun main(): Int {
                    let a = 1
                    let b = 1
                    return a + b
                }
            """
    )

    async with flow_client(host="localhost", port=3569) as client:
        await client.execute_script(
            script=script
            # , block_id
            # , block_height
        )
    
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