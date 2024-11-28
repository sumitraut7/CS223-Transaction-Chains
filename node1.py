# SuperFastPython.com
# example of an asyncio websocket server with websockets
import asyncio
from warnings import catch_warnings
import json
import websockets
import aiomysql


async def get_db_connection():
    # Establish connection to MySQL using asyncio and aiomysql
    return await aiomysql.connect(
        host='localhost',       # Database host
        port=3306,              # Port (default MySQL port)
        user='root',            # Username
        password='root2000',    # Password
        db='server1',           # Database name
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
            # result = await cursor.fetchall()
            # return result
    except Exception as e:
        print(f'An unexpected error occurred : {e}')
    finally:
        connection.close()

# client connection handler
async def client_handler(ws):
    # report client connected
    print(f'Client connected: {ws.remote_address}')
    # read messages from the server and send them back
    async for message in ws:
        # report message
        print(f'> {json.loads(message)}')
        # send message back to client
        await ws.send(message)
    # report client disconnected
    print(f'Client disconnected: {ws.remote_address}')

async def handle_chops():
    query = "SELECT * FROM customers"
    params = ()
    results = await run_query(query,params)
    for row in results:
        print(row)


# drive the server
async def main():

    async with websockets.serve(client_handler, '127.0.0.1', 8080):
        # report progress
        print('Server Started, Control-C to stop')
        # accept connections forever
        await asyncio.Future()


# start the event loop
asyncio.run(main())