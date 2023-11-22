import pygame
import websockets
import asyncio
import argparse
import threading
import json
from itertools import repeat

import utils.utils as utils
from utils.soundManager import SoundManager

from serviceLocator import ServiceLocator
from inputHandler import InputHandler
from actors.madeline import Player
from actors.particles import ParticleManager
from spriteClass import SpriteClass
from constants.enums import ActorTypes,PlayerOrientation



from map.map import Map
from map.titleScreen import drawTitleScreen

import server

from constants.dictionaries import WIDTH, HEIGHT

SCALE = 1
FRAMERATE = 60



async def gameloop(url, port):

    serviceLocator = ServiceLocator()

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
    madeline2 = SpriteClass(0,0,50,50,ActorTypes.PLAYER,"idle1",playerName="Badeline")
    print(madeline2)
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
                print("quit")

            if event.type == pygame.USEREVENT:
                x,y,height,width,spriteID,orientation = event.message
                madeline2.update(x,y,height,width,spriteID,orientation,playerName="Badeline")

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
        madeline2.draw(display)
        

        particlemanager.draw("snow", display)

        #keep track of current frame
        serviceLocator.frameCount += 1
        if serviceLocator.frameCount == framerate:
            serviceLocator.frameCount = 0
        # print(serviceLocator.frameCount)
        uri= f"ws://{url}:{port}"
        async with websockets.connect(uri) as websocket:
            orientation = madeline.orientation == PlayerOrientation.LEFT
            attributes = [
                madeline.x,
                madeline.y,
                madeline.height,
                madeline.spriteWidth,
                madeline.spriteID,
                orientation
            ]
            await websocket.send(json.dumps(attributes))
            


            



        display_shake.blit(display, next(serviceLocator.offset))
        pygame.display.update()

        time += clock.tick(framerate)
        # print(clock.get_fps())


def start_server(loop,future, port):
    loop.run_until_complete(server.main(future, port))

def stop_server(loop,future):
    loop.call_soon_threadsafe(future.set_result, None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game')
    parser.add_argument('--port', type=int, default=8765, help='port number')
    parser.add_argument('--p2ip', type=str, default="127.0.0.1", help='host')
    parser.add_argument('--p2port', type=int, default=8765, help='port number')

    parser.add_argument('--player', type=int, default=1, help='player number')


    args = parser.parse_args()

    print(f"I am {args.port} and I am connecting to {args.p2ip}:{args.p2port}")

    loop = asyncio.get_event_loop()
    future = loop.create_future()
    thread = threading.Thread(target=start_server, args=(loop,future, args.port))
    thread.start()

    asyncio.run(gameloop(args.p2ip, args.p2port))

    stop_server(loop,future)
    thread.join()
    pygame.quit()

    

