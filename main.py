import pygame
from inputHandler import InputHandler
from serviceLocator import ServiceLocator
from madeline import Player
from map import Map

WIDTH, HEIGHT = 800, 800
SCALE = 1
FRAMERATE = 60
display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

clock = pygame.time.Clock()

#Sercice discovery
serviceLocator = ServiceLocator()

#input handler
inputHandler = InputHandler(serviceLocator)

map = Map("1")
serviceLocator.map = map

#player
madeline = Player(*map.spawn,"Madeline",serviceLocator)

#add player to the service locator
serviceLocator.player = madeline

#count the frames (used for animations)
frameCount = 0
serviceLocator.frameCount = frameCount


pygame.init()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()    
    inputHandler.handleInput(keys)



    display.fill((0,0,0))
    madeline.draw(display)    
    map.draw(display)


    #keep track of current frame
    serviceLocator.frameCount += 1
    if serviceLocator.frameCount == FRAMERATE:
        serviceLocator.frameCount = 0

    pygame.display.update()
    clock.tick(FRAMERATE)