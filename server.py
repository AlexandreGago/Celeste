import asyncio
import websockets
import pygame
import json
import functools


async def handler(websocket, path, deque):
    async for message in websocket:
        await process_message(websocket, message, deque)

async def process_message(websocket, message, deque):

    if len(deque) == 0:
        await websocket.send("empty")
        await asyncio.sleep(0)
    else:
        position = deque.popleft()
        await websocket.send(json.dumps(position))
        jsonMessage = json.loads(message)
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, message=jsonMessage))

async def main(event, deque, port):
    print("starting server on port: " + str(port))
    #send queue to handler too
    async with websockets.serve(functools.partial(handler, deque=deque), "0.0.0.0", port) as server:
        while not event.is_set():
            await asyncio.sleep(0)
        server.close()
        
    
