/// This script uses the NFTMinter resource to mint a new NFT
/// It must be run with the account that has the minter resource
/// stored in /storage/NFTMinter

// import NonFungibleToken from "NonFungibleToken"
// import NodeNFT from "NodeNFT"
// import MetadataViews from "MetadataViews"
// import FungibleToken from "FungibleToken"


import NonFungibleToken from 0x631e88ae7f1d7c20
import MetadataViews from 0x631e88ae7f1d7c20
import FungibleToken from 0x9a0766d93b6608b7

import NodeNFT from 0xa63112fad5c0e684

transaction(
    name: String,
    description: String,
    thumbnail: String,
) {

    let recipientCollectionRef: &{NonFungibleToken.CollectionPublic}
    let mintingIDBefore: UInt64

    prepare(signer: AuthAccount) {
        self.mintingIDBefore = NodeNFT.totalSupply

        if signer.borrow<&AnyResource>(from: NodeNFT.CollectionStoragePath) == nil {
            signer.save(<- NodeNFT.createEmptyCollection(), to: NodeNFT.CollectionStoragePath)
            signer.link<&AnyResource{NonFungibleToken.CollectionPublic, MetadataViews.ResolverCollection}>(NodeNFT.CollectionPublicPath, target: NodeNFT.CollectionStoragePath)
        }

        self.recipientCollectionRef = signer
            .getCapability(NodeNFT.CollectionPublicPath)
            .borrow<&{NonFungibleToken.CollectionPublic}>()!

    }
    execute {
        NodeNFT.mintNFT(
            recipient: self.recipientCollectionRef,
            name: name,
            description: description,
            thumbnail: thumbnail,
            royalties: [] as [MetadataViews.Royalty]
        )
    }
}