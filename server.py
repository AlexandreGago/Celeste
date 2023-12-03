import asyncio
import websockets
import pygame
import json
import functools


async def handler(websocket, path, queue):
    async for message in websocket:
        await process_message(websocket, message, queue)


async def process_message(websocket, message, queue):
    jsonMessage = json.loads(message)
    pygame.event.post(pygame.event.Event(pygame.USEREVENT, message=jsonMessage))
    print(message)
    #see if queue is not empty
    if not queue.empty():
        #send message to client
        #empty queue and send last message
        element = await queue.get()
        while not queue.empty():
            element = await queue.get()
        await websocket.send(json.dumps(element))
    else:
        #send message to client
        await websocket.send("empty")
    

        

async def main(queue, port):
    print("starting server on port: " + str(port))
    #send queue to handler too
    async with websockets.serve(functools.partial(handler, queue=queue), "0.0.0.0", port):
        while True:
            await asyncio.sleep(0)
