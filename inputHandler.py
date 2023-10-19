import pygame

class Up():
    def move(self, actor):
        actor.move("jump")

class Down():
    def move(self, actor):
        actor.move("crouch")

class Left():
    def move(self, actor):
        actor.move("walkLeft")

class Right():
    def move(self, actor):
        actor.move("walkRight")


class InputHandler():

    p1command = {
        pygame.K_UP : Up(),
        pygame.K_DOWN : Down(),
        pygame.K_LEFT : Left(),
        pygame.K_RIGHT : Right(),
    }

    def __init__(self,serviceDiscovery):
        self._input = None
        self.serviceDiscovery = serviceDiscovery

    def handleInput(self, keys):
        if keys == None:
            # print(self.serviceDiscovery.getPlayer().state)
            self.serviceDiscovery.getPlayer().move("idle")

        keys = self.parsePressedKeys(keys)
        print(keys)
        if keys:
            for key in keys:
                if key in InputHandler.p1command:
                    InputHandler.p1command[key].move(self.serviceDiscovery.getPlayer())
        else:
            self.serviceDiscovery.getPlayer().move("idle")


    def parsePressedKeys(self,keys):
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
            
            #remove opposite directions
            if (pygame.K_RIGHT in newkeys) and (pygame.K_LEFT in newkeys):
                newkeys.remove(pygame.K_RIGHT)
                newkeys.remove(pygame.K_LEFT)
            if (pygame.K_UP in newkeys )and(pygame.K_DOWN in newkeys):
                newkeys.remove(pygame.K_UP)
                newkeys.remove(pygame.K_DOWN)
            if (pygame.K_DOWN in newkeys):
                #remvoe every other key
                newkeys = []
                newkeys.append(pygame.K_DOWN)

        return newkeys
