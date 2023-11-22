import asyncio
import websockets
import pygame
import json
async def handler(websocket, path):
    async for message in websocket:
        await process_message(websocket, message)


async def process_message(websocket, message):
    jsonMessage = json.loads(message)
    pygame.event.post(pygame.event.Event(pygame.USEREVENT, message=jsonMessage))

async def main(future, port):
    async with websockets.serve(handler,"0.0.0.0", port):
        await future
