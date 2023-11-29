import pygame
from itertools import repeat

import utils.utils as utils
from utils.soundManager import SoundManager

from serviceLocator import ServiceLocator
from inputHandler import InputHandler
from actors.madeline import Player
from actors.particles import ParticleManager

from map.map import Map
from map.titleScreen import drawTitleScreen


from constants.dictionaries import WIDTH, HEIGHT
        
SCALE = 1
FRAMERATE = 60
#Sercice discovery
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

level = 25
map = Map(str(level),serviceLocator)
serviceLocator.map = map
mapCanvas = pygame.Surface((map.width,map.height))
camera = pygame.Rect(0, 0, WIDTH, HEIGHT)


#player
madeline = Player(*map.spawn,"Madeline",serviceLocator)
# madeline2 = Player(*map.spawn,"Badeline",serviceLocator)

#add player to the service locator
serviceLocator.players.append(madeline)
serviceLocator.actorList.append(madeline)

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

bgColor = map.bgColor
display_shake.fill(bgColor)
display.fill(bgColor)

while running:
    
    keys = pygame.key.get_pressed()
    #!Bullet time
    if keys[pygame.K_v]:
        framerate = 1
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
            if event.key==pygame.K_c:
                keys.append(pygame.K_c)
            if event.key == pygame.K_p:
                keys.append(pygame.K_p)
                
    if madeline.levelComplete() or pygame.K_p in keys:
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
    mapCanvas.fill(bgColor)

    

    #manage input
    inputHandler.handleInput(keys)  
      
    particlemanager.update(time)
        

    particlemanager.draw("snow", mapCanvas)
    particlemanager.draw("cloud", mapCanvas)#draw clouds

    map.draw(mapCanvas) # draw the map

    #draw and update actors
    for actor in serviceLocator.actorList:
        actor.update()
        actor.draw(mapCanvas)

    #keep track of current frame
    serviceLocator.frameCount += 1
    if serviceLocator.frameCount == framerate:
        serviceLocator.frameCount = 0
        
    #! Update the camera's position based on the player's position
    camera.x = serviceLocator.players[0].x - WIDTH // 2
    camera.y = serviceLocator.players[0].y - HEIGHT // 2

    #! Ensure the camera stays within the bounds of the map
    camera.x = max(0, min(camera.x, map.width - WIDTH))
    camera.y = max(0, min(camera.y, map.height - HEIGHT))
    
    display.blit(mapCanvas,(0 - camera.x, 0 - camera.y))
    display_shake.blit(display, next(serviceLocator.offset))
    
    pygame.display.update()

    time += clock.tick(framerate)
    # print(clock.get_fps())