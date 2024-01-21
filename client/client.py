import asyncio
import websockets

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.connection = None

    async def connect(self):
        self.connection = await websockets.connect(self.uri)

    async def send_request(self, message):
        if not self.connection:
            raise Exception("Connection not established. Call connect() first.")

        await self.connection.send(message)
        response = await self.connection.recv()
        return response

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
