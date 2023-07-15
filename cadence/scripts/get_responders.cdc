// This script reads the balance field
// of an account's ExampleToken Balance

import MainContractV2 from "MainContractV2"

pub fun main(): {Address: MainContractV2.Responder} {
    // let account = getAccount(address)
    // let vaultRef = account.getCapability(ExampleToken.VaultPublicPath)
    //     .borrow<&ExampleToken.Vault{FungibleToken.Balance}>()
    //     ?? panic("Could not borrow Balance reference to the Vault")

    return MainContractV2.getResponders()
}