// This script reads the balance field
// of an account's FlowNetToken Balance

import FlowNet from "FlowNet"

pub fun main(address: Address): UInt64? {
    // let account = getAccount(address)
    // let vaultRef = account.getCapability(FlowNetToken.VaultPublicPath)
    //     .borrow<&FlowNetToken.Vault{FungibleToken.Balance}>()
    //     ?? panic("Could not borrow Balance reference to the Vault")

    return FlowNetkedOf(address: address)
}