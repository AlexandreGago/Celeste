import random
import pygame

# from actors.madeline import Player
from constants.enums import ActorTypes
# from map.map import Map

def screen_shake(intensity:int, amplitude:int, times:int):
    """
    Function that calculates the screen shake

    Args:
        intensity (int): intensity of the shake
        amplitude (int): amplitude of the shake
        times (int): how many times the shake will happen

    Yields:
        tuple: x and y position of the shake

    """
    direction = -1
    y_shake=1
    for _ in range(0, times):
        y_shake = random.randint(-1, 1)
        for x in range(0, amplitude, intensity):
            yield x * direction, y_shake*x
        for x in range(amplitude, 0, intensity):
            yield x * direction, y_shake*x
        direction *= -1
    while True:
        yield 0, 0

def parsePressedKeys(keys):
    newkeys = []
    if keys :
        if keys[pygame.K_UP]:
            newkeys.append(pygame.K_UP)
        if keys[pygame.K_DOWN]:
            newkeys.append(pygame.K_DOWN)
        if keys[pygame.K_LEFT]:
            newkeys.append(pygame.K_LEFT)
        if keys[pygame.K_RIGHT]:
            newkeys.append(pygame.K_RIGHT)
        if keys[pygame.K_w]:
            newkeys.append(pygame.K_w)
        if keys[pygame.K_s]:
            newkeys.append(pygame.K_s)
        if keys[pygame.K_a]:
            newkeys.append(pygame.K_a)
        if keys[pygame.K_d]:
            newkeys.append(pygame.K_d)
        if keys[pygame.K_1]:
            newkeys.append(pygame.K_1)
        if keys[pygame.K_2]:
            newkeys.append(pygame.K_2)
        
        #remove opposite directions
        if (pygame.K_RIGHT in newkeys) and (pygame.K_LEFT in newkeys):
            newkeys.remove(pygame.K_RIGHT)
            newkeys.remove(pygame.K_LEFT)
        if (pygame.K_UP in newkeys )and(pygame.K_DOWN in newkeys):
            newkeys.remove(pygame.K_UP)
            newkeys.remove(pygame.K_DOWN)
        if (pygame.K_w in newkeys )and(pygame.K_s in newkeys):
            newkeys.remove(pygame.K_w)
            newkeys.remove(pygame.K_s)
        if (pygame.K_a in newkeys )and(pygame.K_d in newkeys):
            newkeys.remove(pygame.K_a)
            newkeys.remove(pygame.K_d)

    return newkeys

def addObservers(serviceLocator) -> None:
    """
    Function that adds observers to the player

    Args:
        serviceLocator (ServiceLocator): ServiceLocator object

    Returns:
        None
    """
    for actor in serviceLocator.actorList:
        for player in serviceLocator.players:
            if actor.type == ActorTypes.DASH_RESET:
                player.add_observer(actor)
            if actor.type == ActorTypes.STRAWBERRY:
                player.add_observer(actor)
            if actor.type == ActorTypes.SPRING:
                player.add_observer(actor)
            if actor.type == ActorTypes.FALLINGBLOCK:
                player.add_observer(actor)
            if actor.type == ActorTypes.DASH_UPGRADE:
                player.add_observer(actor)
            if actor.type == ActorTypes.DOUBLE_DASH_RESET:
                player.add_observer(actor)

