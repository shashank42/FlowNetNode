/// This script uses the NFTMinter resource to mint a new NFT
/// It must be run with the account that has the minter resource
/// stored in /storage/NFTMinter

// import NonFungibleToken from "NonFungibleToken"
// import ExampleNFT from "ExampleNFT"
// import MetadataViews from "MetadataViews"
// import FungibleToken from "FungibleToken"


import NonFungibleToken from 0x631e88ae7f1d7c20
import MetadataViews from 0x631e88ae7f1d7c20
import FungibleToken from 0x9a0766d93b6608b7

import ExampleNFT from 0x250ed09c50c9c6de

transaction(
    name: String,
    description: String,
    thumbnail: String,
) {

    let recipientCollectionRef: &{NonFungibleToken.CollectionPublic}
    let mintingIDBefore: UInt64

    prepare(signer: AuthAccount) {
        self.mintingIDBefore = ExampleNFT.totalSupply

        if signer.borrow<&AnyResource>(from: ExampleNFT.CollectionStoragePath) == nil {
            signer.save(<- ExampleNFT.createEmptyCollection(), to: ExampleNFT.CollectionStoragePath)
            signer.link<&AnyResource{NonFungibleToken.CollectionPublic, MetadataViews.ResolverCollection}>(ExampleNFT.CollectionPublicPath, target: ExampleNFT.CollectionStoragePath)
        }

        self.recipientCollectionRef = signer
            .getCapability(ExampleNFT.CollectionPublicPath)
            .borrow<&{NonFungibleToken.CollectionPublic}>()!

    }
    execute {
        ExampleNFT.mintNFT(
            recipient: self.recipientCollectionRef,
            name: name,
            description: description,
            thumbnail: thumbnail,
            royalties: [] as [MetadataViews.Royalty]
        )
    }
}