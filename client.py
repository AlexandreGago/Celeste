import asyncio
import websockets
import argparse
import pygame
import json

async def client(queue,ip, port):
    websocket = await websockets.connect(f"ws://{ip}:{port}")
    while True:
        if not queue.empty():
            await websocket.send(json.dumps(queue.get_nowait()))
            await asyncio.sleep(0)
            message = await websocket.recv()
            if message == "empty":
                pass
            else:
                jsonMessage = json.loads(message)
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, message=jsonMessage))
        else:
            await asyncio.sleep(0)
# # Run the client
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Websocket Client')
#     parser.add_argument('--port', type=int, default=8765, help='port number')
#     args = parser.parse_args()
#     asyncio.run(client(args.port))