#this has a class that will load a map from the maps.json and determine the sprites to be drawn
#it will also determine the collision map for the map
import pygame.sprite
from actors.dashResetEntity import DashResetEntity
from actors.strawberry import Strawberry
from actors.spring import Spring
from actors.spike import Spike
import json
import base64
levels = json.load(open("maps.json"))
spritesheet = pygame.image.load("atlas.png")
WALLS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A"]
DECORATIONS = ["x", "y", "z"]
ENEMIES = ["o"]
POWERS = ["r","q","s"]

spritelocations = {
    "x": (105,28, 6,4),
    "y": (114,25, 5,7),
    "z": (121,26, 6,6),

    "A" : (0,24, 8,8),

    "a" : (32,16, 8,8),
    "b" : (0,16, 8,8),
    "c" : (39,16, 4,4),
    "d" : (48,16, 8,8),

    "1": (8,16, 6,8),
    "2": (14,16, 6,8),
    "3": (8,24, 6,8),
    "4": (14,24, 6,8),

    "5": (64,32, 4,4),
    "6": (68,32, 4,4),
    "7": (64,36, 4,4),
    "8": (68,36, 4,4),

    "9": (56,16, 8,8),
    "0": (56,24, 8,8),

    "e": (20,16, 6,8),
    "f": (26,16, 6,8),
    "g": (20,24, 6,8),
    "h": (26,24, 6,8),

    "i": (0,32, 8,8),
    "j": (8,32, 8,8),
    "k": (0,40, 8,8),
    "l": (8,40, 8,8),

    "m": (32,24, 12, 8),
    "n": (44,24, 12, 8),

    

} 

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image =  image
        self.rect  =  self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    


class Map:

    def __init__(self, level, servicelocator):
        self.level = level
        self.servicelocator = servicelocator
        self.sprites, self.spawn, self.walls = self.load(level)


    
    def load(self, level):
        sprites = pygame.sprite.Group()
        walls = []
        spawn = None
        # #decode b64
        # level=base64.b64decode(levels[level])
        # #convert to string
        # level=level.decode()
        # #split every 16 characters
        # level=[level[i:i+16] for i in range(0, len(level), 16)]
        # print(level)
        
        level = levels[level]
        for idx,row in enumerate(level):
            for idy,cell in enumerate(row):
                if cell == "p":
                    spawn = (idy*50, idx*50)
                if cell in WALLS:
                    # print(cell)
                    # print(spritelocations[cell])
                    image = spritesheet.subsurface(*spritelocations[cell])
                    #50*16=800
                    image = pygame.transform.scale(image, (50, 50))
                    tile = Tile(image, idy*50, idx*50)
                    sprites.add(tile)
                    walls.append(tile)
                
                elif cell in DECORATIONS:
                    #?scaling is 6x for decorations
                    scale = 6
                    x = spritelocations[cell][2] *scale
                    y = spritelocations[cell][3] *scale
                    
                    image = spritesheet.subsurface(*spritelocations[cell])
                    image = pygame.transform.scale(image, (x, y))
                    sprites.add(Tile(image, idy*50 + ((50-x)/2), idx*50 + (50-y)))
                elif cell in ENEMIES:
                    # image = spritesheet.subsurface(*spritelocations[cell])
                    # image = pygame.transform.scale(image, (50, 50))
                    # sprites.add(Tile(image, idy*50, idx*50))
                    if cell == "o":
                        spike = Spike(idy*50, idx*50)
                        self.servicelocator.actorList.append(spike)
                
                elif cell in POWERS:
                    if cell == "r":
                        dr = DashResetEntity(idy*50, idx*50)
                        self.servicelocator.actorList.append(dr)
                    if cell == "q":
                        s = Strawberry(idy*50, idx*50)
                        self.servicelocator.actorList.append(s)
                    if cell == "s":
                        sp = Spring(idy*50, idx*50)
                        self.servicelocator.actorList.append(sp)

        return sprites, spawn, walls
    
    def draw(self, screen):
        self.sprites.draw(screen)

