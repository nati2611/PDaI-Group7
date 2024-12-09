import asyncio
import websockets
import json
import tornado.web
from tornado.websocket import WebSocketHandler
import tornado.platform.asyncio

# List of connected clients
clients = {}

class MyWebSocketHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("Client connected")

    def on_message(self, message):
        print("Received message:", message)
        # Uncomment to send a response back to the client
        # self.write_message(json.dumps({ "type": "message", "user": "Server", "data": "Hello from server"}))

    def on_close(self):
        print("Client disconnected")

# Function to broadcast a message to all connected clients
async def broadcast_message(message):
    if clients:
        await asyncio.wait([client.send(message) for client in clients.values()])

# Function to handle incoming WebSocket connections
async def handle_client(websocket):
    # Register the client
    client_name = f"Client-{len(clients) + 1}"
    clients[client_name] = websocket
    print(f"{client_name} connected.")

    try:
        async for message in websocket:
            # Parse incoming message
            print("received something!")
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

# Start the WebSocket server
async def start_tornado_server():
    """Start the Tornado WebSocket server."""
    print("Starting Tornado WebSocket server...")
    
    # Integrate Tornado with asyncio
    tornado.platform.asyncio.AsyncIOMainLoop().install()

    # Create the Tornado application
    app = tornado.web.Application([
        (r"/websocket", MyWebSocketHandler),
    ])
    app.listen(8888)
    print("WebSocket server started on ws://localhost:8888/websocket")

    # Keep the server running
    await asyncio.Future()  # Equivalent to running forever

# Entry point
if __name__ == "__main__":
    asyncio.run(start_tornado_server())
    # while True:
    #     print("elo")