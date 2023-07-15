import json
import asyncio
from model_runner import run_model
from flow_py_sdk import flow_client, Script
from flow_py_sdk import cadence


async def get_requests():
    script = Script(
        code="""
                import MainContract from 0x0fb46f70bfa68d94
                pub fun main(): {UInt64: MainContract.Request} {
                    return MainContract.getRequests()
                }
            """
    )

    async with flow_client(host="access.devnet.nodes.onflow.org", port=9000) as client:
        return await client.execute_script(
            script=script
            # , block_id
            # , block_height
        )

async def get_responses():
    script = Script(
        code="""
                import MainContract from 0x0fb46f70bfa68d94
                pub fun main(): {UInt64: MainContract.Response} {
                    return MainContract.getResponses()
                }
            """
    )

    async with flow_client(host="access.devnet.nodes.onflow.org", port=9000) as client:
        return await client.execute_script(
            script=script
            # , block_id
            # , block_height
        )


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(poll_interval):
    while True:
        requests = await get_requests()
        responses = await get_responses()
        
        print(requests.value[0].value)
        # print(requests.value[0].value.fields["responder"])
        
        # print("Name: {}".format(requests.value[0].fields[2].value))
        # print("Address: {}".format(requests.value[0].fields[2].bytes.hex()))
        # print("Balance: {}".format(requests.value[0].fields[3].value))
        
        # prompt = requests.value[0].value.fields["prompt"]
        print(requests.value)
        print(responses.value)
        
        for requestId in requests.value:
            print(requestId.key)
            if requestId not in responses.value:
                run_model(requests.value[int(requestId.key)].value.fields["prompt"], request_id.key)
            
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main_loop():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(2)))
    finally:
        # close loop to free up system resources
        loop.close()
