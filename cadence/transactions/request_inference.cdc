// import MainContractV2 from "MainContractV2"
// import ExampleToken from "ExampleToken"
// import FungibleToken from "FungibleToken"


import MainContractV2 from 0x0fb46f70bfa68d94
import ExampleToken from 0x0fb46f70bfa68d94
import FungibleToken from 0x9a0766d93b6608b7


transaction(responder: Address, prompt: String, offer: UInt64){

    // The Vault resource that holds the tokens that are being transferred
    let sender: @ExampleToken.Vault
    let vault: Capability //<&ExampleToken.Vault{FungibleToken.Receiver}>
    /// Reference to the Fungible Token Receiver of the recipient
    let tokenReceiver: &{FungibleToken.Receiver}
    let address: Address


    prepare(signer: AuthAccount){

        self.sender <- signer.borrow<&ExampleToken.Vault>(from: ExampleToken.VaultStoragePath)!.withdraw(amount: UFix64(offer)) as! @ExampleToken.Vault

        // Get the account of the recipient and borrow a reference to their receiver
        var account = getAccount(0x0fb46f70bfa68d94)
        self.tokenReceiver = account
            .getCapability(ExampleToken.ReceiverPublicPath)
            .borrow<&{FungibleToken.Receiver}>()
            ?? panic("Unable to borrow receiver reference")

        self.vault = signer.getCapability(ExampleToken.ReceiverPublicPath)

        self.address = signer.address
    }

    execute{
        MainContractV2.requestInference(
            prompt: prompt, 
            requestor: self.address,
            responder: responder,
            offer: offer,
            requestorVault: <- self.sender,
            receiverCapability: self.tokenReceiver
        )

    }
}