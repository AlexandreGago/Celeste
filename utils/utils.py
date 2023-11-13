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
        # #if crouched, remain crouched
        # if (pygame.K_DOWN in newkeys):
        #     newkeys = []
        #     newkeys.append(pygame.K_DOWN)

    return newkeys