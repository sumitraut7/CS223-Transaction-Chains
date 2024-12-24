# client.py
import asyncio


import websockets


from transactions import evaluation_set
from config import SERVERS
import time
from datetime import datetime
import json
from transactions import chops
import csv

client_id = 0

start_time = None
execution_time = {}
csv_file = "execution_times.csv"

SERVERS = {
    0: "ws://127.0.0.1:8080",
    1: "ws://127.0.0.1:8081",
    2: "ws://127.0.0.1:8082",
    3: "ws://127.0.0.1:8083",
    4: "ws://127.0.0.1:8084",
    5: "ws://127.0.0.1:8085",
    6: "ws://127.0.0.1:8086",
    7: "ws://127.0.0.1:8087",
}

global_counter = 0


def log(msg):
    print(f"[{datetime.now()}][Client] {msg}")

def log_execution_time(task, received_time, start_time):
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([task, received_time, start_time])

# client connection handler
async def handler(websocket):
    global execution_time
    global start_time
    """Handle incoming WebSocket messages."""
    async for message in websocket:
        try:
            # Parse the JSON message
            msg = json.loads(message)
            if "ABORTING" in msg[0]:
                log(f'{msg[0]}')
            else:
                received_time = datetime.fromisoformat(msg[1])
                transactionID = msg[-1]
                execution_time[transactionID] = (transactionID, received_time-start_time)
                log_execution_time(transactionID, received_time, start_time)
                log(f'Received Message : {msg[0]}')

        except json.JSONDecodeError:
            print(f"Failed to decode message: {message}")


async def send_chain_request(transaction, chain):
    global global_counter
    """
    Send the chain execution request to the first node.
    Send counter for 1st hop of every transaction
    """
    first_server_id = chain[0][1]
    address = SERVERS[first_server_id]
    # message = f"{transaction}|{','.join(map(str, chain))}|1|{global_counter}"
    message = {
        'transaction': transaction,
        'chain': chain,
        'current_index': 1,
        'counter': global_counter
    }

    global_counter+=1
    async with websockets.connect(address) as websocket:
        await websocket.send(json.dumps(message))
        # log(f"{transaction} from Client sent to Node {first_server_id}: {message}")
        log(f"{transaction} from Client sent to Node {first_server_id}")

async def send_multiple_chains():
    global execution_time
    global start_time
    """Send multiple chain execution requests concurrently."""
    # Define multiple chains and tasks
    chains = [(chop, chops[chop]) for i, chop in enumerate(chops)]
    '''
    t1 [1,3,4,2]
    t2 [4,1]
    '''

    # Create coroutines for all chain requests
    tasks = [send_chain_request(task, chain) for task,chain in chains]

    # Run all tasks concurrently
    start_time = datetime.now()
    await asyncio.gather(*tasks)

    log("All chain execution requests sent.")

async def display_responses():
    global execution_time
    while True:
        await asyncio.sleep(5)  # Display every 10 seconds
        print("Recorded Execution times:")
        for client, response in execution_time.items():

            print(f"{client}: {response}")

async def evaluation():
    global execution_time
    global start_time

    evaluation_transactions = {}
    for i in range(0,380):
        appointment_id = 600+i
        patient_id = 500+i
        doctor_id = 400+i
        hop3_modified = (evaluation_set['T1'][-1][0], evaluation_set['T1'][-1][1], [appointment_id,patient_id,doctor_id,('2024-12-01 10:00:00'), ('scheduled')])
        evaluation_transactions[f'T{1+i}']=[evaluation_set['T1'][0],evaluation_set['T1'][1],hop3_modified]

    chains = [(chop, evaluation_transactions[chop]) for i, chop in enumerate(evaluation_transactions)]

    tests = [10,20,50,100,200]
    curr = 0
    for i in tests:
        tasks = []
        for j in range(i):
            task,chain = chains[j+curr]
            tasks.append(send_chain_request(task,chain))
        start_time = datetime.now()
        log(f"{i} chain execution requests sent for evaluating latency.")

        await asyncio.gather(*tasks)
        await asyncio.sleep(i+100)
        curr+=i


    # tasks = [send_chain_request(task, chain) for task, chain in chains]


    log("Evaluation Complete!!!!")

async def start_server():
    """Start the WebSocket server."""

    port = int(SERVERS[client_id].split(":")[-1])
    async with websockets.serve(handler, "localhost", port):
        print('Server Started, Control-C to stop')
        print(f"Client is running on {SERVERS[client_id]}")
        asyncio.create_task(send_multiple_chains())
        # asyncio.create_task(evaluation())
        # asyncio.create_task(display_responses())

        await asyncio.Future()  # Keep the server running


if __name__ == "__main__":
    asyncio.run(start_server())

