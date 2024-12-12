#!/usr/bin/env python

"""Client using the asyncio API."""

import asyncio
from websockets.asyncio.client import connect

# http://192.168.1.162/
async def hello():
    async with connect("ws://192.168.1.203:8888/websocket") as websocket:
        await websocket.send('{ "type":"message", "user":"Artur", "data":"Hello world"}')
        # message = await websocket.recv()
        # print(message)


if __name__ == "__main__":
    asyncio.run(hello())


"""
async def handle_client(websocket):
    # Register the client
    client_name = f"Client-{len(clients) + 1}"
    clients[client_name] = websocket
    print(f"{client_name} connected.")

    try:
        async for message in websocket:
            # Parse incoming message
            print("Processing received message...")
            data = json.loads(message)
            msg_type = data.get("type")
            user = data.get("user")
            msg_data = data.get("data")

            if msg_type == "message":
                # Determine sender and broadcast the message
                sender_name = user
                response = json.dumps({
                    "type": "message",
                    "user": sender_name,
                    "data": msg_data,
                })
                print(f"Broadcasting message: {response}")
                # await broadcast_message(response)
            elif msg_type == "typing":
                # Broadcast typing indicator
                response = json.dumps({
                    "type": "typing",
                    "user": user,
                })
                print(f"Broadcasting typing indicator: {response}")
                await broadcast_message(response)
    except websockets.ConnectionClosed:
        print(f"{client_name} disconnected.")
    finally:
        # Unregister the client
        del clients[client_name]
"""