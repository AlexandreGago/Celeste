import pygame
import websockets
import asyncio
import argparse
from itertools import repeat

import utils.utils as utils
from utils.soundManager import SoundManager

from serviceLocator import serviceLocator
from inputHandler import InputHandler
from actors.madeline import Player
from actors.particles import ParticleManager

from map.map import Map
from map.titleScreen import drawTitleScreen


from constants.dictionaries import WIDTH, HEIGHT

SCALE = 1
FRAMERATE = 60
#Sercice discovery
peers = []
async def gameloop(port, host):
    
    serviceLocator = serviceLocator()

    offset = repeat((0,0))
    display_shake = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
    display = display_shake.copy()
    serviceLocator.display = display

    clock = pygame.time.Clock()

    #input handler
    inputHandler = InputHandler(serviceLocator)

    #sound manager
    soundManager = SoundManager()
    serviceLocator.soundManager = soundManager

    level = 1
    map = Map(str(level),serviceLocator)
    serviceLocator.map = map

    #player
    madeline = Player(*map.spawn,"Madeline",serviceLocator)
    # madeline2 = Player(*map.spawn,"Badeline",serviceLocator)

    #add player to the service locator
    serviceLocator.players.append(madeline)
    serviceLocator.actorList.append(madeline)

    # serviceLocator.players.append(madeline2)
    # serviceLocator.actorList.append(madeline2)

    #count the frames (used for animations)
    frameCount = 0
    serviceLocator.frameCount = frameCount


    particlemanager = ParticleManager()
    particlemanager.add_particles("snow", 50)
    particlemanager.add_particles("cloud", 15)

    time = 0

    #!service locator offset and screen shake function
    serviceLocator.offset = offset

    pygame.init()

    #adds the observers to the players
    utils.addObservers(serviceLocator)

    running = True
    framerate = FRAMERATE

    serviceLocator.soundManager.play("song1", loop=True, volume=0.03)

    drawTitleScreen(display,display_shake,clock,particlemanager)

    running = True
    display_shake.fill((0,0,0))
    display.fill((0,0,0))
    
    server = await websockets.serve(handle_connection, host, port)
    while running:
        display.fill((0,0,0,255))

        if madeline.levelComplete():
            print("completed level")
            level+=1
            serviceLocator.actorList = []
            map = Map(str(level),serviceLocator)
            serviceLocator.map = map

            serviceLocator.players = []
            madeline = Player(*map.spawn,"Madeline",serviceLocator)
            serviceLocator.players.append(madeline)
            serviceLocator.actorList.append(madeline)

            print(serviceLocator.map)

            utils.addObservers(serviceLocator)
            

        
        #parse keys and send to input handler
        keys = pygame.key.get_pressed()

        #!Bullet time
        if keys[pygame.K_v]:
            framerate = 5
        else:
            framerate = FRAMERATE
        #!#####################
        
        #parse the currently pressed keys into a list
        keys = utils.parsePressedKeys(keys)   
        for event in pygame.event.get():# we use the pygame.event to only allow one input per press on the jump and dash keys
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_x:
                    keys.append(pygame.K_x)
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    keys.append(pygame.K_c)
        #manage input
        inputHandler.handleInput(keys)  
        
        particlemanager.update(time)
            
        particlemanager.draw("cloud", display)#draw clouds

        map.draw(display) # draw the map

        #draw and update actors
        for actor in serviceLocator.actorList:
            actor.update()
            actor.draw(display)

        particlemanager.draw("snow", display)
        
        #keep track of current frame
        serviceLocator.frameCount += 1
        if serviceLocator.frameCount == framerate:
            serviceLocator.frameCount = 0
        
        await send_position(madeline, port)

        for ws in peers:
            position = await receive_position(ws)
            print(position)
        
        
        display_shake.blit(display, next(serviceLocator.offset))
        pygame.display.update()

        time += clock.tick(framerate)
        # print(clock.get_fps())

async def handle_connection(websocket,path):
    try:
        async for message in websocket:
            # Broadcast received position to all connected clients
            for ws in peers:
                if ws != websocket:
                    await ws.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass

async def send_position(position, port):
    uri = f"ws://localhost:{port}"
    async with websockets.connect(uri) as websocket:
        await websocket.send(f"{position[0]},{position[1]}")

async def receive_position(websocket):
    message = await websocket.recv()
    return tuple(map(int, message.split(",")))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game')
    parser.add_argument('--port', type=int, default=8765, help='port number')
    parser.add_argument('--host', type=str, default="localhost", help='host')
    args = parser.parse_args()
    asyncio.run(gameloop(args.port, args.host))