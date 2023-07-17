// This transaction is a template for a transaction to allow
// anyone to add a Vault resource to their account so that
// they can use the exampleToken

import FungibleToken from "FungibleToken"
import FlowNetToken from "FlowNetToken"
import MetadataViews from "MetadataViews"
import FlowNet from "FlowNet"

transaction () {
    let vault: Capability<&FlowNetToken.Vault{FungibleToken.Receiver}>
    prepare(signer: AuthAccount){
        self.vault = signer.getCapability<&FlowNetToken.Vault{FungibleToken.Receiver}>(FlowNetToken.ReceiverPublicPath)
    } execute{
        FlowNet.setUpRecieverVault(
            requestorVault: vault
        )
    }
}