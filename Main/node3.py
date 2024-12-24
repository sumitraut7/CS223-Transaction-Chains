import asyncio
import json
from datetime import datetime

import websockets
import time
import aiomysql
import heapq


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

server_id = 3
# Priority queue to store messages
message_queue = []

# Lock for thread-safe queue operations
queue_lock = asyncio.Lock()

async def process_messages():
    """Continuously process messages from the queue."""
    while True:
        await asyncio.sleep(0.1)  # Short delay to prevent busy-waiting

        async with queue_lock:
            if message_queue:
                # Get the message with the lowest number
                _, message = heapq.heappop(message_queue)

                transaction, chain, current_index, counter = parse_message(message)
                # log(f"Processing hop: {chain[current_index-1][0]} with params {chain[current_index-1][-1]}")
                log(f"Processing hop-{current_index} for Transaction-{transaction} where query:{chain[current_index-1][0]}")

                result = await run_query(chain[current_index-1][0], chain[current_index-1][-1])
                if current_index==1 and result==False:
                    msg = f'First Hop FAILED on server {server_id} hence ABORTING transaction-{transaction}'
                    await send_message_to_client((msg, None, None), SERVERS[0])
                else:
                    await process_task(transaction, chain, int(current_index), counter)
                # Process the message (e.g., simulate some processing delay)
                await asyncio.sleep(1)

def log(msg):
    print(f"[{datetime.now()}][Server {server_id}] {msg}")

async def send_message_to_client(message, address):

    try:
        async with websockets.connect(address) as websocket:
            # print(f'Connected to server : {address}')
            await websocket.send(json.dumps(message))

            log(f'Informed Client about completion of Transaction {message[-1]} ')
    except websockets.exceptions.ConnectionClosedError as e:
        print(f'Connection to server {address} closed unexpectedly : {e}')
    except Exception as e:
        print(f'An error occurred while communicating with the server {address}: {e}')


async def handler(websocket):
    """Handle incoming WebSocket messages."""
    async for message in websocket:
        try:
            # Parse the JSON message
            msg = json.loads(message)
            counter = msg.get("counter")  # Extract the counter

            if counter is not None:
                async with queue_lock:
                    # Add the message to the priority queue
                    heapq.heappush(message_queue, (counter, msg))
                log(f"Received and queued message: {msg.get('transaction')}|Counter:{msg.get('counter')}")
            else:
                print(f"Invalid message format: {message}")
        except json.JSONDecodeError:
            print(f"Failed to decode message: {message}")



# async def handler(websocket):
#     """Handle incoming messages from other nodes."""
#     async for message in websocket:
#         log(f"Node {server_id} received: {message}")
#         transaction, chain, current_index, counter = parse_message(message)
#         print(transaction, chain, current_index, counter)
#         await process_task(transaction, chain, int(current_index), counter)

async def get_db_connection():
    # Establish connection to MySQL using asyncio and aiomysql
    return await aiomysql.connect(
        host='localhost',       # Database host
        port=3306,              # Port (default MySQL port)
        user='root',            # Username
        password='root2000',    # Password
        db='s3',                # Database name
        autocommit=True         # Event loop (using the asyncio event loop)
    )

async def run_query(query, params):
    """
    Execute a SELECT query asynchronously.
    :param query: SQL query string with placeholders (e.g., 'SELECT * FROM table WHERE id = %s').
    :param params: Parameters for the query (tuple or list).
    :return: List of rows fetched from the database.
    """
    connection = await get_db_connection()
    try:
        async with connection.cursor() as cursor:  # Use DictCursor for row as dictionary
            await cursor.execute(query, params or ())
            result = await cursor.fetchall()
            log(f'Query Execution Output: {result}')
            return True
    except Exception as e:
        print(f'An unexpected error occurred : {e}')
        return False
    finally:
        connection.close()

async def process_task(transaction, chain, current_index, counter):
    """Process the task and forward it to the next server in the chain."""

    if current_index < len(chain):

        next_server_id = chain[current_index][1]
        log(f"Node {server_id} forwarding task to Node {next_server_id}")
        await send_task(chain, current_index+1, transaction, counter)
    else:
        log(f"Node {server_id} completed task: {transaction}")
        msg,completion_time = f"Node {server_id} completed task: {transaction}", datetime.now().isoformat()
        await send_message_to_client((msg,completion_time,transaction),SERVERS[0])

async def send_task(chain, current_index, transaction, counter):
    """Send the task to the next server in the chain."""
    next_server_id = chain[current_index - 1][1]
    address = SERVERS[next_server_id]
    message = create_message(chain, current_index, transaction, counter)
    async with websockets.connect(address) as websocket:
        await websocket.send(json.dumps(message))
        # log(f"Node {server_id} sent to Node {next_server_id}: {message}")
        log(f"Node {server_id} sent to Node {next_server_id}")

def create_message(chain, current_index, transaction, counter):
    """Format the message to send."""
    message = {
        'transaction': transaction,
        'chain': chain,
        'current_index': current_index,
        'counter': counter
    }

    return message

def parse_message(message):
    """Parse the incoming message."""
    # message = json.loads(message)
    transaction, chain, current_index, counter = message['transaction'], message['chain'], message['current_index'], message['counter']
    return transaction, chain, current_index, counter

async def start_server():
    """Start the WebSocket server."""

    port = int(SERVERS[server_id].split(":")[-1])
    async with websockets.serve(handler, "localhost", port):
        print('Server Started, Control-C to stop')
        print(f"Node {server_id} is running on {SERVERS[server_id]}")
        asyncio.create_task(process_messages())
        await asyncio.Future()  # Keep the server running

if __name__ == "__main__":

    asyncio.run(start_server())
