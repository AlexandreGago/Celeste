#simple message websockets server
import asyncio
import websockets

async def handler(websocket, path):
    async for message in websocket:
        await process_message(websocket, message)
    
async def process_message(websocket, message):
    print(message)
    
async def main(future, port):
    async with websockets.serve(handler,"0.0.0.0", port):
        await future
        
        
if __name__ == "__main__":
    future = asyncio.Future()
    asyncio.ensure_future(main(future,8765))
    asyncio.get_event_loop().run_forever()