import tornado.web
import tornado.platform.asyncio
import asyncio
from tornado.websocket import WebSocketHandler
import threading

class MyWebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("Client connected")

    def on_message(self, message):
        print("Received message:", message)

    def on_close(self):
        print("Client disconnected")

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
    # asyncio.run(start_tornado_server())
    print("cos")
    websocket_thread = threading.Thread(target=asyncio.run(start_tornado_server()))
    websocket_thread.start()

