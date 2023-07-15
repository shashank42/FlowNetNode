import MainContract from "MainContract"
import ExampleToken from "ExampleToken"
import FungibleToken from "FungibleToken"
import NonFungibleToken from "NonFungibleToken"
import InferenceNFT from "InferenceNFT"

transaction(
    id: UInt64,
    url: String,
    ){ 
    let tokenReciever: &{FungibleToken.Receiver}
    let NFTRecievingCapability: &{NonFungibleToken.CollectionPublic}
    let minter: &InferenceNFT.NFTMinter
    let senderVault: Capability<&ExampleToken.Vault>
    let address: Address

    prepare(signer: AuthAccount){

        self.senderVault = signer.getCapability<&ExampleToken.Vault>(/private/exampleTokenVault)

        self.tokenReciever = account
            .getCapability(ExampleToken.ReceiverPublicPath)
            .borrow<&{FungibleToken.Receiver}>()
            ?? panic("Unable to borrow receiver reference")

        self.NFTRecievingCapability = getAccount(signer.address).getCapability(InferenceNFT.CollectionPublicPath) 
                        .borrow<&InferenceNFT.Collection{NonFungibleToken.CollectionPublic}>()
                        ?? panic("Failed to get User's collection.")

        self.minter = signer.borrow<&InferenceNFT.NFTMinter>(from: InferenceNFT.MinterStoragePath)
            ?? panic("Account does not store an object at the specified path")

        self.address = signer.address

    }
    execute{
        MainContract.recieveInference(
        id: id, 
        url: url, 
        responder: self.address,
        tokenProvider: self.senderVault,
        responderRecievingCapability: self.tokenReciever,
        responderNFTRecievingCapability: self.NFTRecievingCapability,
        minter: self.minter
        )
    }
}

