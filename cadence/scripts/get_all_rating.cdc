// This script reads the balance field
// of an account's FlowNetToken Balance

import FlowNet from 0xa63112fad5c0e684

pub fun main(address: Address): {UInt64: FlowNet.Rating} {
    return FlowNet.getAllRatings()
}