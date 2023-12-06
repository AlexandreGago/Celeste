import pygame
from constants.enums import ActorTypes

class InputHandler():
    _instance = None
    p1command = {
        pygame.K_UP : (0,1,0,0),
        pygame.K_DOWN : (0,-1,0,0),
        pygame.K_LEFT : (-1,0,0,0),
        pygame.K_RIGHT : (1,0,0,0),
        pygame.K_c : (0,0,0,-1),
        pygame.K_x : (0,0,1,0),
        "idle": (0,0,0,0)
    }
    p2command = {
        pygame.K_w : (0,1,0,0),
        pygame.K_s : (0,-1,0,0),
        pygame.K_a : (-1,0,0,0),
        pygame.K_d : (1,0,0,0),
        pygame.K_1 : (0,0,0,-1),
        pygame.K_2 : (0,0,1,0),
        "idle": (0,0,0,0)
    }
    
    def __new__(cls, servicelocator) -> 'InputHandler':
        if cls._instance is not None:
            raise ValueError("An instance of InputHandler already exists")
        cls._instance = super(InputHandler, cls).__new__(cls)
        return cls._instance
        

    def __init__(self,serviceLocator):
        self._input = None
        self.serviceLocator = serviceLocator

    def handleInput(self, keys):
        if keys:
            #sum the directions
            for player in self.serviceLocator.getPlayers():
                if player.name == "Madeline":
                    vector = [0,0,0,0]
                    for key in keys:
                        if key in self.p1command:
                            vector[0] += self.p1command[key][0]
                            vector[1] += self.p1command[key][1]
                            vector[2] += self.p1command[key][2]
                            vector[3] += self.p1command[key][3]
                    player.move(tuple(vector))
                elif player.name == "Badeline":
                    vector = [0,0,0,0]
                    for key in keys:
                        if key in self.p2command:
                            vector[0] += self.p2command[key][0]
                            vector[1] += self.p2command[key][1]
                            vector[2] += self.p2command[key][2]
                            vector[3] += self.p2command[key][3]
                    player.move(tuple(vector))

            
        else:
            for player in self.serviceLocator.getPlayers():
                player.move(self.p1command["idle"])



