import random
import pygame
def screen_shake(intensity, amplitude, times):
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
        if keys[pygame.K_c]:
            newkeys.append(pygame.K_c)
        
        #remove opposite directions
        if (pygame.K_RIGHT in newkeys) and (pygame.K_LEFT in newkeys):
            newkeys.remove(pygame.K_RIGHT)
            newkeys.remove(pygame.K_LEFT)
        if (pygame.K_UP in newkeys )and(pygame.K_DOWN in newkeys):
            newkeys.remove(pygame.K_UP)
            newkeys.remove(pygame.K_DOWN)

        #if crouched, remain crouched
        if (pygame.K_DOWN in newkeys):
            newkeys = []
            newkeys.append(pygame.K_DOWN)

    return newkeys