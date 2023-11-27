import pygame
import websockets
import asyncio
import argparse
import threading
import json
import pickle
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
#!--------------------
# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# s.close()
#!--------------------

#this is the main game loop that runs the game and multiplayer logic
async def gameloop(coop:bool, mp:bool,url:str, port:int):
    """Summary
    This is the main game loop that runs the game and multiplayer logic

    Args:
        coop (bool) : whether or not to run the game in coop mode
        mp (bool)  : whether or not to run the game in multiplayer mode
        url (str)  : ip address of player 2
        port (int) : port number of player 2
    """
    #this is the service locator that is used to pass around the game objects
    serviceLocator = ServiceLocator()

    #this is the offset that is used to shake the screen
    offset = repeat((0,0))
    serviceLocator.offset = offset
    #this is the display that is used to shake the screen
    display_shake = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
    #this is the display that is used to draw the game
    display = display_shake.copy()
    #actors will be drawn to display
    serviceLocator.display = display
    #clock is used to run the game at a constant framerate
    clock = pygame.time.Clock()

    #input handler
    inputHandler = InputHandler(serviceLocator)

    #sound manager
    soundManager = SoundManager()
    serviceLocator.soundManager = soundManager

    #player 1 level
    level = 1
    #load the first map
    map = Map(str(level),serviceLocator)
    #add the map to the service locator
    serviceLocator.map = map

    #Player 1 object
    madeline = Player(*map.spawn,"Madeline",serviceLocator)
    serviceLocator.players.append(madeline)
    serviceLocator.actorList.append(madeline)
    
    #player 2 is a sprite that will be updated if we are in multiplayer
    if mp:
        madeline2 = SpriteClass(0,0,50,50,ActorTypes.PLAYER,"idle1",playerName="Badeline")
    
    #if coop is true, add player 2 to the service locator
    if coop:
        madeline2 = Player(*map.spawn,"Badeline",serviceLocator)
        serviceLocator.players.append(madeline2)
        serviceLocator.actorList.append(madeline2)

    #count the frames (used for animations)
    frameCount = 0
    serviceLocator.frameCount = frameCount

    #particle manager manages clouds and snow
    particlemanager = ParticleManager()
    particlemanager.add_particles("snow", 50)
    particlemanager.add_particles("cloud", 15)
    time = 0
    

    #initialize pygame
    pygame.init()

    #adds the observers to the players
    utils.addObservers(serviceLocator)

    #running is used to determine if the game is running
    running = True
    #framerate is used to determine the framerate of the game
    framerate = FRAMERATE

    #play bg music
    serviceLocator.soundManager.play("song1", loop=True, volume=0.03)

    #title screen until the user presses space
    drawTitleScreen(display,display_shake,clock,particlemanager)

    #clear the screen after the title screen
    bgColor = map.bgColor
    display_shake.fill(bgColor)
    display.fill(bgColor)

    #if we are in multiplayer, connect to the other player
    if mp:
        uri= f"ws://{url}:{port}"
        websocket = await websockets.connect(uri)
        p2level = 1
        
    while running:
        #get the pressed keys
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
                x,y,height,width,spriteID,orientation, p2level = event.message
                madeline2.update(x,y,height,width,spriteID,orientation,playerName="Badeline")

            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_x:
                    keys.append(pygame.K_x)
                if event.key==pygame.K_c:
                    keys.append(pygame.K_c)
                if event.key == pygame.K_p:
                    keys.append(pygame.K_p)

        if madeline.levelComplete()or pygame.K_p in keys:
            print("completed level")
            level+=1
            serviceLocator.actorList = []
            map = Map(str(level),serviceLocator)
            serviceLocator.map = map
            bgColor = map.bgColor

            for player in serviceLocator.players:
                serviceLocator.actorList.append(player)
                player.reset(*map.spawn)
                print(player.x,player.y)


            utils.addObservers(serviceLocator)


        display.fill(bgColor)

        #manage input
        inputHandler.handleInput(keys)
        particlemanager.update(time)
        particlemanager.draw("cloud", display)#draw clouds
        map.draw(display) # draw the map

        #draw and update actors
        for actor in serviceLocator.actorList:
            actor.update()
            actor.draw(display)
        
        if mp and p2level == level:
            madeline2.draw(display)
        

        particlemanager.draw("snow", display)

        #keep track of current frame
        serviceLocator.frameCount += 1
        if serviceLocator.frameCount == framerate:
            serviceLocator.frameCount = 0
        # print(serviceLocator.frameCount)
        if mp:
                hairpoints = madeline.hairPoints
                orientation = madeline.orientation == PlayerOrientation.LEFT
                attributes = [
                    madeline.x,
                    madeline.y,
                    madeline.height,
                    madeline.width,
                    madeline.spriteID,
                    orientation,
                    # madeline.hairPoints,
                    # madeline.particles,
                    level
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
    parser.add_argument('--mp', type=bool, default=False, help='multiplayer')
    parser.add_argument('--coop', type=bool, default=False, help='coop')
    parser.add_argument('--port', type=int, default=8765, help='port number')
    parser.add_argument('--p2ip', type=str, default="127.0.0.1", help='host')
    parser.add_argument('--p2port', type=int, default=8765, help='port number')

    parser.add_argument('--player', type=int, default=1, help='player number')


    args = parser.parse_args()
    #mp and coop are mutually exclusive
    if args.mp and args.coop:
        print("mp and coop are mutually exclusive")
        exit()

    if args.mp:            
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        thread = threading.Thread(target=start_server, args=(loop,future, args.port))
        thread.start()

        asyncio.run(gameloop(args.coop,args.mp,args.p2ip, args.p2port))

        stop_server(loop,future)
        thread.join()
        pygame.quit()
    else:
        asyncio.run(gameloop(args.coop,args.mp,args.p2ip, args.p2port))
        pygame.quit()

    

