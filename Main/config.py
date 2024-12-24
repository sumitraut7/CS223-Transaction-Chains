# config.py
import asyncio
from websockets import connect

SERVERS = {
    1: "ws://127.0.0.1:8081",
    2: "ws://127.0.0.1:8082",
    3: "ws://127.0.0.1:8083",
    4: "ws://127.0.0.1:8084",
    5: "ws://127.0.0.1:8085",
    6: "ws://127.0.0.1:8085",
    7: "ws://127.0.0.1:8085",
}

async def connect_to_server(server_id):
    """Connect to another server using WebSocket."""
    uri = SERVERS[server_id]
    return await connect(uri)

