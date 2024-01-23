import asyncio
import websockets

class WebSocketManager:
    _instance = None
    _websocket = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebSocketManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    async def get_websocket(cls, uri="ws://localhost:1423"):
        if not cls._websocket or cls._websocket.closed:
            cls._websocket = await websockets.connect(uri)
        return cls._websocket

    @classmethod
    async def send_to_websocket(cls, data, uri="ws://localhost:1423"):
        """Send data to the WebSocket server and wait for a response."""
        websocket = await cls.get_websocket(uri)
        await websocket.send(data)
        return await websocket.recv()
