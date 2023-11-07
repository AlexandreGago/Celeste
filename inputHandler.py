import pygame
from constants.enums import ActorTypes
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
        pygame.K_UP : (0,1,0,0),
        pygame.K_DOWN : (0,-1,0,0),
        pygame.K_LEFT : (-1,0,0,0),
        pygame.K_RIGHT : (1,0,0,0),
        pygame.K_c : (0,0,0,-1),
        pygame.K_x : (0,0,1,0),
        "idle": (0,0,0,0)
    }

    def __init__(self,serviceDiscovery):
        self._input = None
        self.serviceDiscovery = serviceDiscovery

    def handleInput(self, keys):

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



