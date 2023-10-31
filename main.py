import pygame
from inputHandler import InputHandler
from serviceLocator import serviceLocator
from actors.madeline import Player
from map.map import Map
from actors.dashResetEntity import DashResetEntity
from actors.particles import ParticleManager
from constants.enums import ActorTypes
from states import *

from itertools import repeat

WIDTH, HEIGHT = 800, 800
SCALE = 1
FRAMERATE = 10
#Sercice discovery
serviceLocator = serviceLocator()

offset = repeat((0,0))
display_shake = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
display = display_shake.copy()
serviceLocator.display = display

clock = pygame.time.Clock()


#input handler
inputHandler = InputHandler(serviceLocator)

map = Map("1",serviceLocator)
serviceLocator.map = map

#player
madeline = Player(*map.spawn,"Madeline",serviceLocator)

#add player to the service locator
serviceLocator.player = madeline
serviceLocator.actorList.append(madeline)

#count the frames (used for animations)
frameCount = 0
serviceLocator.frameCount = frameCount


particlemanager = ParticleManager()
particlemanager.add_particles("snow", 50)
particlemanager.add_particles("cloud", 15)

time = 0

#add 
for actor in serviceLocator.actorList:
    actor.update()

    if actor.type == ActorTypes.DASH_RESET:
        serviceLocator.player.add_observer(actor)
    if actor.type == ActorTypes.STRAWBERRY:
        serviceLocator.player.add_observer(actor)
    if actor.type == ActorTypes.SPRING:
        serviceLocator.player.add_observer(actor)


#!service locator offset and screen shake function
serviceLocator.offset = offset

pygame.init()
running = True
is_spawned = False

#! MEGA PORCO
target = madeline.y
madeline.y=800
def spawn(player,spawned):
    if madeline.y > target:    
        madeline.y -= 8
    else:
        global is_spawned
        return True
    return False

framerate = 60

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    keys = pygame.key.get_pressed()   
    if keys[pygame.K_v]:
        framerate = 5 
    else:
        framerate = 60
    display.fill((0,0,0))
    particlemanager.update(time)

    #let input be considered after spawning animation is done
    if is_spawned:
        inputHandler.handleInput(keys)
    else:
        is_spawned = spawn(madeline,is_spawned)
        madeline.sprite.update(madeline.x, madeline.y,madeline.height,madeline.width,madeline.spriteID,madeline.orientation==1)
        
        
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
    if serviceLocator.frameCount == FRAMERATE:
        serviceLocator.frameCount = 0

    display_shake.blit(display, next(serviceLocator.offset))
    pygame.display.update()
    
    

    time += clock.tick(framerate)