import asyncio
import websockets

async def websocket_client(uri="ws://localhost:8000"):
    """A WebSocket client to receive and process messages."""
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            process_message(message)

def process_message(message):
    """Process the received message."""
    print(f"Received message: {message}")
    # Add your processing logic here

if __name__ == "__main__":
    asyncio.run(websocket_client())
