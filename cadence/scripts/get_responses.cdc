// This script reads the balance field
// of an account's FlowNetToken Balance

import FlowNet from 0xd868d023029053e1
pub fun main(): {UInt64: FlowNet.Response} {
    return FlowNet.getResponses()
}