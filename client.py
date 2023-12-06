import asyncio
import websockets
import pygame
import json

async def client(event,deque,ip, port):
    websocket = await websockets.connect(f"ws://{ip}:{port}")
    while not event.is_set():        
        if len(deque) == 0:
            await asyncio.sleep(0)
        else:
            position = deque.popleft()
            await websocket.send(json.dumps(position))
            message = await websocket.recv()
            if message == "empty":
                pass
            else:
                jsonMessage = json.loads(message)
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, message=jsonMessage))
    websocket.close()
            