
// import MainContractV2 from "MainContractV2"
// import ExampleToken from "ExampleToken"
// import FungibleToken from "FungibleToken"
// import ExampleNFT from "ExampleNFT"
// import NonFungibleToken from "NonFungibleToken"
// import InferenceNFT from "InferenceNFT"


import MainContractV2 from 0x250ed09c50c9c6de
import ExampleToken from 0x250ed09c50c9c6de
import FungibleToken from 0x9a0766d93b6608b7
import ExampleNFT from 0x250ed09c50c9c6de
import NonFungibleToken from 0x631e88ae7f1d7c20
import InferenceNFT from 0x250ed09c50c9c6de


transaction(id: UInt64, rating: UInt64){ //type: String, url: String

    // The Vault resource that holds the tokens that are being transferred
    // let reciever: @ExampleToken.Vault
    let vault: Capability //<&ExampleToken.Vault{FungibleToken.Receiver}>
    /// Reference to the Fungible Token Receiver of the recipient
    // let tokenProvider: &{FungibleToken.Provider}
    let tokenReciever: &{FungibleToken.Receiver}
    let NFTRecievingCapability: &{NonFungibleToken.CollectionPublic}
    let minter: &ExampleToken.Minter

    let senderVault: Capability<&ExampleToken.Vault>

    let address: Address

    prepare(signer: AuthAccount){

        // self.sender <- signer.borrow<&ExampleToken.Vault>(from: ExampleToken.VaultStoragePath)!.withdraw(amount: UFix64(1)) as! @ExampleToken.Vault

        // Get the account of the recipient and borrow a reference to their receiver
        var account = getAccount(0xf8d6e0586b0a20c7)
        // self.tokenProvider = account
        //     .getCapability(ExampleToken.VaultStoragePath)
        //     .borrow<&{FungibleToken.Provider}>()
        //     ?? panic("Unable to borrow provider reference")

        self.senderVault = signer.getCapability<&ExampleToken.Vault>(/private/exampleTokenVault)


        self.tokenReciever = signer
            .getCapability(ExampleToken.ReceiverPublicPath)
            .borrow<&{FungibleToken.Receiver}>()
            ?? panic("Unable to borrow receiver reference")

        self.vault = signer.getCapability(ExampleToken.ReceiverPublicPath)

        self.NFTRecievingCapability = getAccount(signer.address).getCapability(InferenceNFT.CollectionPublicPath) 
                        .borrow<&InferenceNFT.Collection{NonFungibleToken.CollectionPublic}>()
                        ?? panic("Failed to get User's collection.")

        // Borrow a reference to the Minter resource in storage
        self.minter = signer.borrow<&ExampleToken.Minter>(from: ExampleToken.MinterStoragePath)
            ?? panic("Account does not store an object at the specified path")

        self.address = signer.address

    }
    execute{
        MainContractV2.rateInference(
            id: id, 
            rating: rating,
            minter: self.minter,
            receiverCapability: self.tokenReciever,
            rater: self.address
        )
    }
}





