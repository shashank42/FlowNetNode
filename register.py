import os
from contract import fContract
from chain import handle_event, web3, Web3
from model import get_pinata_object
from flow_py_sdk import flow_client, AccountKey, signer, ProposalKey, cadence, Tx
import asyncio

def register_on_contract(cost):
    
    # Get account
    # web3.eth.account.enable_unaudited_hdwallet_features()
    # mnemonic = ""
    # with open('mnemonic.txt') as f:
    #     lines = f.readlines()
    #     mnemonic = lines[0]
    # account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/539'/0'/0/0")
    
    # account1, signer1 = AccountKey.from_seed(
    #         sign_algo=signer.SignAlgo.ECDSA_P256,
    #         hash_algo=signer.HashAlgo.SHA3_256,
    #         seed=mnemonic,
    #     )
    
    pinata = get_pinata_object()
    image_ipfs = pinata.pin_file_to_ipfs("node.png")
    file_ipfs = pinata.pin_file_to_ipfs("model.py")
    
    metadata_json = {
        "name": "Flow AI Node",
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
    # chain_id = web3.eth.chain_id
    # tx = fContract.functions.registerResponder(cost, metadata_ipfs["IpfsHash"]).buildTransaction({
    #     "chainId": chain_id,
    #     'nonce': web3.eth.getTransactionCount(account.address),
    #     'from': account.address
    # })
    # print(tx)
    # signed_tx = web3.eth.account.signTransaction(tx, private_key=account.key)

    # sentTx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                register_responder(metadata_ipfs["IpfsHash"], image_ipfs["IpfsHash"])))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close() 
    
    
    
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




async def register_responder(
    url: str,
    img: str
):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
        

        web3.eth.account.enable_unaudited_hdwallet_features()
        mnemonic = ""
        with open('mnemonic.txt') as f:
            lines = f.readlines()
            mnemonic = lines[0]

        account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/539'/0'/0/0")
                
        account_address, new_signer = AccountKey.from_seed(
                sign_algo=signer.SignAlgo.ECDSA_P256,
                hash_algo=signer.HashAlgo.SHA3_256,
                seed=mnemonic,
        )
        
        latest_block = await client.get_latest_block()
        proposer = await client.get_account_at_latest_block(
            address=account_address.bytes
        )
        cost = cadence.Int(1)
        url = cadence.String(url)
        name = cadence.String("Flow AI Node")
        description = cadence.String("Decentralized AI inference nodes")
        thumbnail = cadence.String(img)
        
        transaction = (
            Tx(
                code="""
                import MainContract from 0x0fb46f70bfa68d94
                import NonFungibleToken from 0x631e88ae7f1d7c20
                import ExampleNFT from 0x0fb46f70bfa68d94

                transaction( 
                    cost: Int, 
                    url: String, 
                    name: String,
                    description: String,
                    thumbnail: String,
                ){ 
                    let NFTRecievingCapability: &{NonFungibleToken.CollectionPublic}
                    let minter: &ExampleNFT.NFTMinter
                    let address: Address

                    prepare(signer: AuthAccount){
                        self.address = signer.address
                        self.NFTRecievingCapability = getAccount(signer.address).getCapability(ExampleNFT.CollectionPublicPath) 
                                        .borrow<&ExampleNFT.Collection{NonFungibleToken.CollectionPublic}>()
                                        ?? panic("Failed to get User's collection.")

                        // borrow a reference to the NFTMinter resource in storage
                        self.minter = signer.borrow<&ExampleNFT.NFTMinter>(from: ExampleNFT.MinterStoragePath)
                            ?? panic("Account does not store an object at the specified path")
                    }
                    execute {
                        MainContract.registerResponder(
                            cost: UInt64(cost), 
                            url: url, 
                            responder: self.address,
                            recipient: self.NFTRecievingCapability,
                            name: name,
                            description: description,
                            thumbnail: url,
                            minter: self.minter
                        )
                    }
                }
                """,
                reference_block_id=latest_block.id,
                payer=account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[0].sequence_number,
                ),
            )
            .add_arguments(cost)
            .add_arguments(url)
            .add_arguments(name)
            .add_arguments(description)
            .add_arguments(thumbnail)
            .with_envelope_signature(
                account_address,
                0,
                new_signer,
            )
        )

        await client.execute_transaction(transaction)
    
    

