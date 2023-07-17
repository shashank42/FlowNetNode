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
import FlowNetToken from 0xa63112fad5c0e684
import MetadataViews from 0x631e88ae7f1d7c20
import NodeNFT from 0xa63112fad5c0e684
import InferenceNFT from 0xa63112fad5c0e684
import NonFungibleToken from 0x631e88ae7f1d7c20


transaction () {

    prepare(signer: AuthAccount) {

        
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

            // // Create a public capability to the Vault that only exposes
            // // the deposit function through the Receiver interface
            // signer.link<&FlowNetToken.Vault{FungibleToken.Provider}>(
            //     FlowNetToken.VaultPublicPath,
            //     target: FlowNetToken.VaultStoragePath
            // )
        }

        // Return early if the account already stores a FlowNetToken Vault
        if signer.borrow<&NodeNFT.Collection>(from: NodeNFT.CollectionStoragePath) != nil {
            
        } else {
            log("Create a new NodeNFT EmptyCollection and put it in storage")
            // Create a new FlowNetToken Vault and put it in storage
            signer.save(
                <-NodeNFT.createEmptyCollection(),
                to: NodeNFT.CollectionStoragePath
            )

            // Create a public capability to the Vault that only exposes
            // the deposit function through the Receiver interface
            signer.link<&NodeNFT.Collection{NonFungibleToken.Receiver}>(
                NodeNFT.CollectionPublicPath,
                target: NodeNFT.CollectionStoragePath
            )

            // // Create a public capability to the Vault that exposes the Balance and Resolver interfaces
            // signer.link<&NodeNFT.Vault{FungibleToken.Balance, MetadataViews.Resolver}>(
            //     NodeNFT.CollectionPublicPath,
            //     target: NodeNFT.CollectionStoragePath
            // )

            // // Create a public capability to the Vault that only exposes
            // // the deposit function through the Receiver interface
            // signer.link<&FlowNetToken.Vault{FungibleToken.Provider}>(
            //     FlowNetToken.VaultPublicPath,
            //     target: FlowNetToken.VaultStoragePath
            // )
        }

        // Return early if the account already stores a FlowNetToken Vault
        if signer.borrow<&InferenceNFT.Collection>(from: InferenceNFT.CollectionStoragePath) != nil {
            
        } else {
            log("Create a new InferenceNFT EmptyCollection and put it in storage")
            // Create a new FlowNetToken Vault and put it in storage
            signer.save(
                <-InferenceNFT.createEmptyCollection(),
                to: InferenceNFT.CollectionStoragePath
            )

            // Create a public capability to the Vault that only exposes
            // the deposit function through the Receiver interface
            signer.link<&InferenceNFT.Collection{NonFungibleToken.Receiver}>(
                InferenceNFT.CollectionPublicPath,
                target: InferenceNFT.CollectionStoragePath
            )

            // // Create a public capability to the Vault that exposes the Balance and Resolver interfaces
            // signer.link<&NodeNFT.Vault{FungibleToken.Balance, MetadataViews.Resolver}>(
            //     NodeNFT.CollectionPublicPath,
            //     target: NodeNFTllectionStoragePath
            // )

            // // Create a public capability to the Vault that only exposes
            // // the deposit function through the Receiver interface
            // signer.link<&FlowNetToken.Vault{FungibleToken.Provider}>(
            //     FlowNetToken.VaultPublicPath,
            //     target: FlowNetToken.VaultStoragePath
            // )
        }
        
    }
}