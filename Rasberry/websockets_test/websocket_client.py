#!/usr/bin/env python

"""Client using the asyncio API."""

import asyncio
from websockets.asyncio.client import connect

# http://192.168.1.162/
async def hello():
    async with connect("ws://localhost:8888") as websocket:
        await websocket.send('{ "type":"message", "user":"Artur", "data":"Hello world"}')
        # message = await websocket.recv()
        # print(message)


if __name__ == "__main__":
    asyncio.run(hello())