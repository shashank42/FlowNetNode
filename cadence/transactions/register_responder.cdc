import MainContract from "MainContract"
import NonFungibleToken from "NonFungibleToken"
import ExampleNFT from "ExampleNFT"

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