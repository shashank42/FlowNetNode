// This transaction is a template for a transaction to allow
// anyone to add a Vault resource to their account so that
// they can use the exampleToken

// import FungibleToken from "FungibleToken"
// import FlowNetToken from "FlowNetToken"
// import MetadataViews from "MetadataViews"
// import NodeNFT from "NodeNFT"
// import InferenceNFT from "InferenceNFT"
// import NonFungibleToken from "NonFungibleToken"

import FungibleToken from 0x9a0766d93b6608b7
import FlowNetToken from 0xd868d023029053e1
import MetadataViews from 0x631e88ae7f1d7c20
import NodeNFT from 0xd868d023029053e1
import InferenceNFT from 0xd868d023029053e1
import NonFungibleToken from 0x631e88ae7f1d7c20


transaction () {

    prepare(signer: AuthAccount) {
        if signer.borrow<&FlowNetToken.Vault>(from: FlowNetToken.VaultStoragePath) != nil {
            
        } else {
            signer.save(
                <-FlowNetToken.createEmptyVault(),
                to: FlowNetToken.VaultStoragePath
            )
            signer.link<&FlowNetToken.Vault{FungibleToken.Receiver}>(
                FlowNetToken.ReceiverPublicPath,
                target: FlowNetToken.VaultStoragePath
            )
            signer.link<&FlowNetToken.Vault{FungibleToken.Balance, MetadataViews.Resolver}>(
                FlowNetToken.VaultPublicPath,
                target: FlowNetToken.VaultStoragePath
            )
        }

        if signer.borrow<&NodeNFT.Collection>(from: NodeNFT.CollectionStoragePath) != nil {
            
        } else {
            signer.save(
                <-NodeNFT.createEmptyCollection(),
                to: NodeNFT.CollectionStoragePath
            )
            signer.link<&NodeNFT.Collection{NonFungibleToken.Receiver}>(
                NodeNFT.CollectionPublicPath,
                target: NodeNFT.CollectionStoragePath
            )
        }

        if signer.borrow<&InferenceNFT.Collection>(from: InferenceNFT.CollectionStoragePath) != nil {
            
        } else {
            log("Create a new InferenceNFT EmptyCollection and put it in storage")
            signer.save(
                <-InferenceNFT.createEmptyCollection(),
                to: InferenceNFT.CollectionStoragePath
            )
            signer.link<&InferenceNFT.Collection{NonFungibleToken.Receiver}>(
                InferenceNFT.CollectionPublicPath,
                target: InferenceNFT.CollectionStoragePath
            )
        }

        // Get the account of the recipient and borrow a reference to their receiver
        var tokenReceiver = signer
            .getCapability(FlowNetToken.ReceiverPublicPath)
            .borrow<&{FungibleToken.Receiver}>()
            ?? panic("Unable to borrow receiver reference")


        let mintedVault <- FlowNetToken.mintTokens(amount: amount)

        // Deposit them to the receiever
        self.tokenReceiver.deposit(from: <-mintedVault)
        
    }
}