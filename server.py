import asyncio
import websockets
import pygame
import json


async def handler(websocket, path):
    async for message in websocket:
        await process_message(websocket, message)


async def process_message(websocket, message):
    # jsonMessage = json.loads(message)
    # pygame.event.post(pygame.event.Event(pygame.USEREVENT, message=jsonMessage))
    print(message)
async def main(queue, port):
    print("starting server on port: " + str(port))
    async with websockets.serve(handler,"0.0.0.0", port):
        while True:
            #peek at the queue to see if there is a message
            if not queue.empty():
                message = queue.get()
            await asyncio.sleep(0)
