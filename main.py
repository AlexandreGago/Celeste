import pygame
from inputHandler import InputHandler
from serviceLocator import serviceLocator
from utils.soundManager import SoundManager

import utils.utils as utils

from actors.madeline3 import Player

from map.map import Map
from actors.dashResetEntity import DashResetEntity
from actors.particles import ParticleManager
from constants.enums import ActorTypes
from states import *

from itertools import repeat

WIDTH, HEIGHT = 800, 800
SCALE = 1
#Sercice discovery
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
framerate = 1

serviceLocator.soundManager.play("song1", loop=True, volume=0.03)
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
        framerate = 60
    #!#####################
        
    keys = utils.parsePressedKeys(keys)   
    for event in pygame.event.get():
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
        
    particlemanager.draw("cloud", display)
    #draw map
    map.draw(display)
    #draw actors
    for actor in serviceLocator.actorList:
        actor.update()
        actor.draw(display)

    particlemanager.draw("snow", display)
    # pygame.draw.rect(display,(255,0,0), madeline.spriteGroup.sprites()[0].rect,1)
    
    #keep track of current frame
    serviceLocator.frameCount += 1
    if serviceLocator.frameCount == framerate:
        serviceLocator.frameCount = 0

    display_shake.blit(display, next(serviceLocator.offset))
    pygame.display.update()
    
    

    time += clock.tick(framerate)
    # print(clock.get_fps())