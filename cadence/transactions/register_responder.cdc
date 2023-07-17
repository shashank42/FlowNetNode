// import MainContractV2 from "MainContractV2"
// import NonFungibleToken from "NonFungibleToken"
// import ExampleNFT from "ExampleNFT"

import MainContractV2 from 0x250ed09c50c9c6de
import NonFungibleToken from 0x631e88ae7f1d7c20
import ExampleNFT from 0x250ed09c50c9c6de
import MetadataViews from 0x631e88ae7f1d7c20


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

        if signer.borrow<&AnyResource>(from: ExampleNFT.CollectionStoragePath) == nil {
            signer.save(<- ExampleNFT.createEmptyCollection(), to: ExampleNFT.CollectionStoragePath)
            signer.link<&AnyResource{NonFungibleToken.CollectionPublic, MetadataViews.ResolverCollection}>(ExampleNFT.CollectionPublicPath, target: ExampleNFT.CollectionStoragePath)
        }

        self.NFTRecievingCapability = signer
            .getCapability(ExampleNFT.CollectionPublicPath)
            .borrow<&{NonFungibleToken.CollectionPublic}>()!
            
    }
    execute {
        MainContractV2.registerResponder(
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