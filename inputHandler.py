import pygame
from enums import ActorTypes
# class Up():
#     def move(self, actor):
#         actor.move((0,-1))

# class Down():
#     def move(self, actor):
#         actor.move((0,1))

# class Left():
#     def move(self, actor):
#         actor.move((-1,0))

# class Right():
#     def move(self, actor):
#         actor.move((1,0))

class InputHandler():

    p1command = {
        pygame.K_UP : (0,0,0,1),
        pygame.K_DOWN : (0,1,0,0),
        pygame.K_LEFT : (-1,0,0,0),
        pygame.K_RIGHT : (1,0,0,0),
        pygame.K_SPACE : (0,-1,0,0),
        pygame.K_LSHIFT : (0,0,1,0),
        "idle": (0,0,0,0)
    }

    def __init__(self,serviceDiscovery):
        self._input = None
        self.serviceDiscovery = serviceDiscovery

    def handleInput(self, keys):

        keys = self.parsePressedKeys(keys)
        if keys:
            #sum the directions
            vector = [0,0,0,0]
            for key in keys:
                vector[0] += self.p1command[key][0]
                vector[1] += self.p1command[key][1]
                vector[2] += self.p1command[key][2]
                vector[3] += self.p1command[key][3]
            self.serviceDiscovery.getPlayer().move(tuple(vector))

            
        else:
            self.serviceDiscovery.getPlayer().move(self.p1command["idle"])
        
        #update actors (animations)
        for actor in self.serviceDiscovery.actorList:
            if actor.type != ActorTypes.PLAYER:
                actor.update()


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
            if keys[pygame.K_SPACE]:
                newkeys.append(pygame.K_SPACE)
            if keys[pygame.K_LSHIFT]:
                newkeys.append(pygame.K_LSHIFT)
            
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
