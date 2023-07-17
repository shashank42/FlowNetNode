
// import FlowNet from "FlowNet"
// import FlowNetToken from "FlowNetToken"
// import FungibleToken from "FungibleToken"
// import NodeNFT from "NodeNFT"
// import NonFungibleToken from "NonFungibleToken"
// import InferenceNFT from "InferenceNFT"

import MetadataViews from 0x631e88ae7f1d7c20
import FlowNet from 0xa63112fad5c0e684
import FlowNetToken from 0xa63112fad5c0e684
import FungibleToken from 0x9a0766d93b6608b7
import NodeNFT from 0xa63112fad5c0e684
import NonFungibleToken from 0x631e88ae7f1d7c20
import InferenceNFT from 0xa63112fad5c0e684


transaction(id: UInt64, rating: UInt64){

    let vault: Capability
    let tokenReciever: &{FungibleToken.Receiver}

    let senderVault: Capability<&FlowNetToken.Vault>

    let address: Address

    prepare(signer: AuthAccount){

        // Return early if the account already stores a FlowNetToken Vault
        if signer.borrow<&FlowNetToken.Vault>(from: FlowNetToken.VaultStoragePath) != nil {
            
        } else {
            log("Create a new FlowNetToken Vault and put it in storage")
            // Create a new FlowNetToken Vault and put it in storage
            signer.save(
                <-FlowNetToken.createEmptyVault(),
                to: FlowNetToken.VaultStoragePath
            )

            // Create a public capability to the Vault that only exposes
            // the deposit function through the Receiver interface
            signer.link<&FlowNetToken.Vault{FungibleToken.Receiver}>(
                FlowNetToken.ReceiverPublicPath,
                target: FlowNetToken.VaultStoragePath
            )

            // Create a public capability to the Vault that exposes the Balance and Resolver interfaces
            signer.link<&FlowNetToken.Vault{FungibleToken.Balance, MetadataViews.Resolver}>(
                FlowNetToken.VaultPublicPath,
                target: FlowNetToken.VaultStoragePath
            )
        }

        self.senderVault = signer.getCapability<&FlowNetToken.Vault>(/private/exampleTokenVault)

        self.tokenReciever = signer
            .getCapability(FlowNetToken.ReceiverPublicPath)
            .borrow<&{FungibleToken.Receiver}>()
            ?? panic("Unable to borrow receiver reference")

        self.vault = signer.getCapability(FlowNetToken.ReceiverPublicPath)


        self.address = signer.address

    }
    execute{
        FlowNet.rateInference(
            id: id, 
            rating: rating,
            receiverCapability: self.tokenReciever,
            rater: self.address
        )
    }
}





