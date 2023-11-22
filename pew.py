import websockets
import asyncio



async def hello():
    uri = "ws://127.0.0.1:8766"
    async with websockets.connect(uri) as websocket:
        await websocket.send("test")


asyncio.get_event_loop().run_until_complete(hello())