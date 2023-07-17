// import FlowNet from "FlowNet"
// import NonFungibleToken from "NonFungibleToken"
// import NodeNFT from "NodeNFT"

import MetadataViews from 0x631e88ae7f1d7c20
import NonFungibleToken from 0x631e88ae7f1d7c20
import FungibleToken from 0x9a0766d93b6608b7

import FlowNet from 0xa63112fad5c0e684
import NodeNFT from 0xa63112fad5c0e684
import FlowNetToken from 0xa63112fad5c0e684
import InferenceNFT from 0xa63112fad5c0e684

transaction( 
    cost: Int, 
    url: String, 
    name: String,
    description: String,
    thumbnail: String,
 ){ 
    let NFTRecievingCapability: &{NonFungibleToken.CollectionPublic}
    let address: Address

    prepare(signer: AuthAccount){
        self.address = signer.address

        if signer.borrow<&AnyResource>(from: NodeNFT.CollectionStoragePath) == nil {
            signer.save(<- NodeNFT.createEmptyCollection(), to: NodeNFT.CollectionStoragePath)
            signer.link<&AnyResource{NonFungibleToken.CollectionPublic, MetadataViews.ResolverCollection}>(NodeNFT.CollectionPublicPath, target: NodeNFT.CollectionStoragePath)
        }

        if signer.borrow<&AnyResource>(from: InferenceNFT.CollectionStoragePath) == nil {
            signer.save(<- InferenceNFT.createEmptyCollection(), to: InferenceNFT.CollectionStoragePath)
            signer.link<&AnyResource{NonFungibleToken.CollectionPublic, MetadataViews.ResolverCollection}>(InferenceNFT.CollectionPublicPath, target: InferenceNFT.CollectionStoragePath)
        }

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
            signer.link<&FlowNetToken.Vault{FungibleToken.Provider}>(
                FlowNetToken.VaultPublicPath,
                target: FlowNetToken.VaultStoragePath
            )
        }  

        self.NFTRecievingCapability = signer
            .getCapability(NodeNFT.CollectionPublicPath)
            .borrow<&{NonFungibleToken.CollectionPublic}>()!
            
    }
    execute {
        FlowNet.registerResponder(
            cost: UInt64(cost), 
            url: url, 
            responder: self.address,
            recipient: self.NFTRecievingCapability,
            name: name,
            description: description,
            thumbnail: url
        )
    }
}