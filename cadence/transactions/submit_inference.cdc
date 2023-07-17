

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

transaction(
    id: UInt64,
    url: String,
    ){ 

    let tokenReciever: &{FungibleToken.Receiver}
    let NFTRecievingCapability: &{NonFungibleToken.CollectionPublic}
    let address: Address

    prepare(signer: AuthAccount){

        self.tokenReciever = signer
            .getCapability(FlowNetToken.ReceiverPublicPath)
            .borrow<&{FungibleToken.Receiver}>()
            ?? panic("Unable to borrow receiver reference")

        if signer.borrow<&AnyResource>(from: InferenceNFT.CollectionStoragePath) == nil {
            signer.save(<- InferenceNFT.createEmptyCollection(), to: InferenceNFT.CollectionStoragePath)
            signer.link<&AnyResource{NonFungibleToken.CollectionPublic, MetadataViews.ResolverCollection}>(InferenceNFT.CollectionPublicPath, target: InferenceNFT.CollectionStoragePath)
        }

        self.NFTRecievingCapability = signer
            .getCapability(InferenceNFT.CollectionPublicPath)
            .borrow<&{NonFungibleToken.CollectionPublic}>()!

        self.address = signer.address

    }
    execute{
        FlowNet.recieveInference(
            id: id, 
            url: url, 
            responder: self.address,
            responderRecievingCapability: self.tokenReciever,
            responderNFTRecievingCapability: self.NFTRecievingCapability,
        )

    }
}

