import pygame
from inputHandler import InputHandler
from serviceLocator import serviceLocator
from actors.madeline import Player
from map.map import Map
from actors.dashResetEntity import DashResetEntity
from actors.snowParticle import ParticleManager
from constants.enums import ActorTypes
from states import *

from itertools import repeat

WIDTH, HEIGHT = 800, 800
SCALE = 1
FRAMERATE = 60
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
particlemanager.add_particles(50)
#dt = delta time
#time = total time
dt = 0
time = 0

#add 
for actor in serviceLocator.actorList:
    if actor.type == ActorTypes.DASH_RESET:
        serviceLocator.player.add_observer(actor)
    if actor.type == ActorTypes.STRAWBERRY:
        serviceLocator.player.add_observer(actor)

states = [Idle(),Walk(),Turning(),Jump(),Dash(),Crouch()]
transitions = []


#!service locator offset and screen shake function
serviceLocator.offset = offset

pygame.init()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()    
    display.fill((0,0,0))

    #update actors
    inputHandler.handleInput(keys)

    #draw actors
    for actor in serviceLocator.actorList:
        actor.draw(display)
    #draw map
    map.draw(display)

    #draw particles
    particlemanager.update(dt,time)
    particlemanager.draw(display)
    
    # pygame.draw.rect(display,(255,0,0), madeline.spriteGroup.sprites()[0].rect,1)


    #keep track of current frame
    serviceLocator.frameCount += 1
    if serviceLocator.frameCount == FRAMERATE:
        serviceLocator.frameCount = 0

    display_shake.blit(display, next(serviceLocator.offset))
    pygame.display.update()
    
    
    # dt = clock.tick(FRAMERATE)/18
    dt = clock.tick(FRAMERATE)/20
    time += dt