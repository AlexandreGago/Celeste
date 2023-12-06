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
import client

from constants.dictionaries import WIDTH, HEIGHT

SCALE = 1
FRAMERATE = 60
WINDOW_WIDTH, WINDOW_HEIGHT = 800,800


def initialize_game(coop:bool, mp:bool, queue: asyncio.Queue = None ):
    """Summary
    This is a function to initialize the game
    """
    #initialize level at 1
    level = 1
    #initialize singletons
    serviceLocator = ServiceLocator()
    inputHandler = InputHandler(serviceLocator)
    soundManager = SoundManager()
    
    
    #initialize clock and map
    clock = pygame.time.Clock()
    game_map = Map(str(level),serviceLocator)
    
    particlemanager = ParticleManager(game_map.width,game_map.height)
    particlemanager.add_particles("snow", 50)
    particlemanager.add_particles("cloud", 15)
    
    #camera is used on bigger levels for scrolling
    camera = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    mapCanvas = pygame.Surface((game_map.width,game_map.height))

    #offset is used for screen shake
    offset = repeat((0,0))
    
    #display is the surface that is drawn to, display_shake is the surface that is drawn to the screen
    #display_shake will draw display with an offset to simulate screen shake
    display_shake = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
    display = display_shake.copy()

    #add variables to serviceLocator
    serviceLocator.soundManager = soundManager
    serviceLocator.display = display
    serviceLocator.offset = offset
    serviceLocator.map = game_map

    #this is initialized here because it needs the map
    madeline = Player(*game_map.spawn,"Madeline",serviceLocator)
    serviceLocator.players.append(madeline)
    serviceLocator.actorList.append(madeline)
    
    p2level = None
    if mp:
        #in multiplayer badeline is only used for drawing
        badeline = SpriteClass(0,0,50,50,ActorTypes.PLAYER,"idle1",playerName="Badeline")
        p2level = 1
    elif coop:
        #here it is an actual player and is added to the list of players
        badeline = Player(*game_map.spawn,"Badeline",serviceLocator)
        serviceLocator.players.append(badeline)
        serviceLocator.actorList.append(badeline)
    else:
        badeline = None
        
    

 
    
    utils.addObservers(serviceLocator)
    
    
    return (
        serviceLocator,
        inputHandler,
        camera,
        clock,
        display,
        display_shake,
        game_map,
        mapCanvas,
        madeline,
        particlemanager,
        level,
        p2level,
        badeline
    )


async def gameloop(coop:bool, mp:bool, queue: asyncio.Queue = None ):
    """Summary
    This is the main game loop that runs the game and multiplayer logic

    Args:
        coop (bool): True if coop is enabled
        mp (bool): True if multiplayer is enabled
        queue (asyncio.LifoQueue, optional): queue used to pass messages between server and client
    """

    (
        serviceLocator,
        inputHandler,
        camera,
        clock,
        display,
        display_shake,
        game_map,
        mapCanvas,
        madeline,
        particlemanager,
        level,
        p2level,
        badeline
    ) = initialize_game(coop,mp,queue)
    
    if coop:
        madelinecomplete = False
        badelinecomplete = False
    else:
        madelinecomplete = False
    
    pygame.init()
    #keys that can't be held down
    no_hold_keys = [pygame.K_x,pygame.K_c,pygame.K_1,pygame.K_2,pygame.K_p]
    time=0
    running = True

    #loop forever level song
    serviceLocator.soundManager.play("song1", loop=True, volume=0.1)
    drawTitleScreen(display,display_shake,clock,particlemanager)

    #clear the screen
    bgColor = game_map.bgColor
    display_shake.fill(bgColor)
    display.fill(bgColor)
    mapCanvas.fill(bgColor)


    while running:        
        keys = pygame.key.get_pressed()
        #!###############
        if keys[pygame.K_v]:
            framerate = 5
        else:
            framerate = FRAMERATE
        #!###############
        keys = utils.parsePressedKeys(keys)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #custom event for multiplayer
            if event.type == pygame.USEREVENT:
                x,y,height,width,spriteID,orientation, p2level = event.message
                badeline.update(x,y,height,width,spriteID,orientation,playerName="Badeline")

            #prevent holding down keys
            if event.type == pygame.KEYDOWN and event.key in no_hold_keys:
                keys.append(event.key)
                
        #go to next level
        if coop:
            madelinecomplete = madeline.levelComplete()  if not madelinecomplete else madelinecomplete
            badelinecomplete = badeline.levelComplete() if not badelinecomplete else badelinecomplete
            levelComplete = madelinecomplete and badelinecomplete
        else:
            levelComplete = madeline.levelComplete()
            
        if levelComplete or pygame.K_p in keys:
            madelinecomplete = False
            badelinecomplete = False
            level+=1
            serviceLocator.actorList = []
            game_map = Map(str(level),serviceLocator)
            serviceLocator.map = game_map
            bgColor = game_map.bgColor

            for player in serviceLocator.players:
                serviceLocator.actorList.append(player)
                player.reset(*game_map.spawn)

            utils.addObservers(serviceLocator)
            particlemanager.setMapSize(game_map.width,game_map.height)


        #reset display on every frame
        display.fill(bgColor)
        mapCanvas.fill(bgColor)

        #move players
        inputHandler.handleInput(keys)
        #update particles
        particlemanager.update(time)
        particlemanager.draw("cloud", mapCanvas)
        particlemanager.draw("snow", mapCanvas)
        
        #update camera
        game_map.draw(mapCanvas) 
        camera.x = serviceLocator.players[0].x - WINDOW_WIDTH // 2
        camera.y = serviceLocator.players[0].y - WINDOW_HEIGHT // 2  
        camera.x = max(0, min(camera.x, game_map.width - WINDOW_WIDTH))
        camera.y = max(0, min(camera.y, game_map.height - WINDOW_HEIGHT))

        #update all actors
        for actor in serviceLocator.actorList:
            actor.update()
            actor.draw(mapCanvas)
        
        #multiplayer logic
        if mp:
            #draw badeline
            badeline.draw(mapCanvas)
            orientation = madeline.orientation == PlayerOrientation.LEFT
            attributes = [
                madeline.x,
                madeline.y,
                madeline.height,
                madeline.width,
                madeline.spriteID,
                orientation, 
                level
            ]
            #put attributes in queue to be sent to other player
            if not queue.full():
                queue.put_nowait(attributes)
            else:
                #replace first message in queue
                queue.get_nowait()
                queue.put_nowait(attributes)

        #put map canvas on display
        display.blit(mapCanvas,(0 - camera.x, 0 - camera.y))
        #put display on display_shake with offset if needed
        display_shake.blit(display, next(serviceLocator.offset))
        pygame.display.update()

        #wait for next frame
        time += clock.tick(framerate)



def start_server(queue,port):
    asyncio.run(server.main(queue,port))
def start_client(queue, ip, port):
    asyncio.run(client.client(queue, ip,port))


 
async def main(*args):
    parser = argparse.ArgumentParser(description='Game')
    # parser.add_argument('--coop', type=bool, default=False, help='coop')
    parser.add_argument('-coop', action='store_true', help='coop')
    parser.add_argument('-mp', action='store_true', help='mp')
    
    parser.add_argument('-port', type=int, default=8765, help='host port number')
    parser.add_argument('-p2ip', type=str, default="None", help='player 2 ip')
    parser.add_argument('-p2port', type=int, default=8765, help='player 2 port number')


    args = parser.parse_args()
    
    if args.mp and args.coop:
        print("mp and coop are mutually exclusive")
        exit()

    if args.mp:          
        import ipaddress
        import socket
        try:
            ipaddress.ip_address(args.p2ip)
        except ValueError:
            print("p2 ip is not valid")
            exit()
            
        sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sc.connect(("8.8.8.8", 80))
        ip = sc.getsockname()[0]
        sc.close()
        ip = ipaddress.ip_address(ip)
        
        #find out who is the server
        server = ip > ipaddress.ip_address(args.p2ip)
        
        #!###############
        if args.p2ip == "127.0.0.1":
            server = False
        #!###############
        print("own ip: " + str(ip))        
        
        queue = asyncio.LifoQueue(maxsize=1)
        loop = asyncio.get_event_loop()
        if server:
            thread = threading.Thread(target=start_server, args=(queue,args.port))
            thread.start()  
        else:
            thread = threading.Thread(target=start_client, args=(queue,args.p2ip, args.p2port))
            thread.start()
            
        await gameloop(args.coop, args.mp, queue)

        thread.join()
        pygame.quit()
    else:
        await gameloop(args.coop,args.mp,None)
        pygame.quit()
    
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
    except Exception as e:
        pygame.quit()
        exit()

