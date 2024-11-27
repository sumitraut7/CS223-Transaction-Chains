

import asyncio
import websockets
import json

from transactions import TransactionChains

node_ports = {
    0: 8080,
    2: 8082,
    3: 8083,
    4: 8084
}


async def send_message_to_node(message, port):
    address = f"ws://127.0.0.1:{port}"
    print(address)
    try:
        async with websockets.connect(address) as websocket:
            print(f'Connected to server : {address}')
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print(f'Response from server {address}: ')
    except websockets.exceptions.ConnectionClosedError as e:
        print(f'Connection to server {address} on port {port} closed unexpectedly : {e}')
    except Exception as e:
        print(f'An error occurred while communicating with the server on port {port}: {e}')


# drive the client connection
async def main():
    # open a connection to the server
    chains = TransactionChains()

    tasks = [send_message_to_node(chains.get_chains('T1'),node_ports.get(0)),
    send_message_to_node(chains.get_chains('T1'), node_ports.get(2)),
    send_message_to_node(chains.get_chains('T1'), node_ports.get(3)),
    send_message_to_node(chains.get_chains('T1'), node_ports.get(4))]

    await asyncio.gather(*tasks)


# start the event loop
asyncio.run(main())