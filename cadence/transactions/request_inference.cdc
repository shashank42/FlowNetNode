// import FlowNet from "FlowNet"
// import FlowNetToken from "FlowNetToken"
// import FungibleToken from "FungibleToken"


import FlowNet from 0xa63112fad5c0e684
import FlowNetToken from 0xa63112fad5c0e684
import FungibleToken from 0x9a0766d93b6608b7


transaction(responder: Address, prompt: String, offer: UInt64){
    let sender: @FlowNetToken.Vault
    let vault: Capability
    let address: Address

    prepare(signer: AuthAccount){

        self.sender <- signer.borrow<&FlowNetToken.Vault>(from: FlowNetToken.VaultStoragePath)!.withdraw(amount: UFix64(offer)) as! @FlowNetToken.Vault

        self.vault = signer.getCapability(FlowNetToken.ReceiverPublicPath)

        self.address = signer.address
    }

    execute{
        FlowNet.requestInference(
            prompt: prompt, 
            requestor: self.address,
            responder: responder,
            offer: offer,
            requestorVault: <- self.sender
        )

    }
}