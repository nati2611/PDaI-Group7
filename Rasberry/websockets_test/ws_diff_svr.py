import tornado.web
from tornado.websocket import WebSocketHandler
import tornado.platform.asyncio
import asyncio
import json

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

# Asynchronous function to perform background tasks
async def periodic_task():
    while True:
        print("Running periodic task...")
        await asyncio.sleep(5)  # Example task that runs every 5 seconds
    await asyncio.sleep(1)

if __name__ == "__main__":
    # Set up Tornado to work with asyncio
    tornado.platform.asyncio.AsyncIOMainLoop().install()

    # Create the Tornado application
    app = tornado.web.Application([
        (r"/websocket", MyWebSocketHandler),
    ])
    app.listen(8888)
    print("WebSocket server started on ws://localhost:8888/websocket")

    # Schedule the periodic task to run
    # asyncio.create_task(periodic_task())

    # # Start the asyncio event loop (Tornado is now integrated with asyncio)
    asyncio.get_event_loop().run_forever()