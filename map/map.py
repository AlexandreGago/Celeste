#this has a class that will load a map from the maps.json and determine the sprites to be drawn
#it will also determine the collision map for the map
import pygame.sprite
from actors.dashResetEntity import DashResetEntity
from actors.strawberry import Strawberry
from actors.spring import Spring
from actors.spike import Spike
from actors.fallingBlock import FallingBlock
from actors.cloud import Cloud
from actors.dashUpgrade import DashUpgrade
from constants.enums import SpikeOrientations
from constants.dictionaries import WIDTH
import json
import base64
levels = json.load(open("./map/maps.json", encoding="utf-8"))
spritesheet = pygame.image.load("atlas.png")
WALLS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A","á","à","Á","À","ã","é","è","É","È","ẽ","Ẽ","ê","Ê","ë","Ë","ē","Ē","ė","Ė","ę","Ę","ĕ","Ĕ"]
DECORATIONS = ["x", "y", "z"]
ENEMIES = ["o", "O", "ó", "ò"]
POWERS = ["r","q","s", "t","u","v"]
SIZE = WIDTH/16

import os

levelBgColors={
    "1": (0,0,0,255),
    "2": (0,0,0,255),
    "3": (0,0,0,255),
    "4": (0,0,0,255),
    "5": (0,0,0,255),
    "6": (0,0,0,255),
    "7": (0,0,0,255),
    "8": (0,0,0,255),
    "9": (0,0,0,255),
    "10": (0,0,0,255),
    "11": (0,0,0,255),
    "12": (0,0,0,255),
    "13": (0,0,0,255),
    "14": (0,0,0,255),
    "15": (0,0,0,255),
    "16": (0,0,0,255),
    "17": (0,0,0,255),
    "18": (0,0,0,255),
    "19": (0,0,0,255),
    "20": (0,0,0,255),
    "21": (0,0,0,255),
    "22": (0,0,0,255),
    "23": (0,0,0,255),
    "24": (0,0,0,255),

    "debug":(0,0,0,255),
    "new":(0,0,0,255)
}
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
    
    "á":(32,16, 8,8),
    "à":(32,16, 8,8),
    "Á":(64,32,8,8),
    "À":(0,24, 8,8),
    "ã":(20,16,12,16),

    "é":(16,32,8,8),
    "è":(24,32,8,8),
    "É":(32,32,8,8),
    "È":(16,40,8,8),
    "ẽ":(24,40,8,8),
    "Ẽ":(32,40,8,8),
    "ê":(16,48,8,8),
    "Ê":(24,48,8,8),
    "ë":(32,48,8,8),
    "Ë":(16,56,8,8),
    "ē":(24,56,8,8),
    "Ē":(32,56,8,8),
    "ė":(40,32,8,8),
    "Ė":(40,40,8,8),
    "ę":(40,48,8,8),
    "Ę":(40,56,8,8),
    "ĕ":(56,16, 8,8),
    "Ĕ":(56,24, 8,8),

}

class Tile(pygame.sprite.Sprite):
    def __init__(self, image:pygame.image, x:int, y:int) -> None:
        """
        Creates a tile object

        Args:
            image (pygame.image): image of the tile
            x (int): x position of the tile
            y (int): y position of the tile

        Returns:
            None

        """
        pygame.sprite.Sprite.__init__(self)
        self.image =  image
        self.rect  =  self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




class Map:

    def __init__(self, level:int, servicelocator) -> None:
        """
        Creates a map object

        Args:
            level (int): level to be loaded
            servicelocator (ServiceLocator): ServiceLocator object

        Returns:
            None

        """
        self.level = level
        self.servicelocator = servicelocator
        self.sprites, self.spawn, self.walls = self.load(level)
        self.bgColor = levelBgColors[str(level)]



    def load(self, level:int) -> tuple[pygame.sprite.Group, tuple[int,int], list]:
        """
        Loads a level from the maps.json file

        Args:
            level (int): level to be loaded

        Returns:
            sprites (pygame.sprite.Group): sprites to be drawn
            spawn (tuple): spawn location
            walls (list): list of walls
        """
        sprites = pygame.sprite.Group()
        walls = []
        
        self.servicelocator.actorList = []
        self.servicelocator.fallingBlocks = []
        self.servicelocator.clouds = []
        
        spawn = None

        self.bgColor = levelBgColors[str(level)]
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
                    spawn = (idy*SIZE, idx*SIZE)
                if cell in WALLS:
                    # print(cell)
                    # print(spritelocations[cell])
                    image = spritesheet.subsurface(*spritelocations[cell])
                    if cell == "á":
                        image = pygame.transform.rotate(image,90)
                    if cell == "à":
                        image = pygame.transform.rotate(image,270)
                    if cell == "À":
                        image = pygame.transform.rotate(image,90)
                    if cell == "ĕ":
                        image = pygame.transform.rotate(image,90)
                    if cell == "Ĕ":
                        image = pygame.transform.rotate(image,90)
                    image = pygame.transform.scale(image, (SIZE, SIZE))
                    #SIZE*16=800
                    tile = Tile(image, idy*SIZE, idx*SIZE)
                    sprites.add(tile)
                    walls.append(tile)

                elif cell in DECORATIONS:
                    #?scaling is 6x for decorations
                    scale = 6
                    x = spritelocations[cell][2] *scale
                    y = spritelocations[cell][3] *scale

                    image = spritesheet.subsurface(*spritelocations[cell])
                    image = pygame.transform.scale(image, (x, y))
                    sprites.add(Tile(image, idy*SIZE + ((SIZE-x)/2), idx*SIZE + (SIZE-y)))
                elif cell in ENEMIES:
                    # image = spritesheet.subsurface(*spritelocations[cell])
                    # image = pygame.transform.scale(image, (SIZE, SIZE))
                    # sprites.add(Tile(image, idy*SIZE, idx*SIZE))
                    if cell in ["o"]:
                        orientation = SpikeOrientations.UP
                    if cell in ["O"]:
                        orientation = SpikeOrientations.DOWN 
                    if cell in ["ó"]:
                        orientation = SpikeOrientations.RIGHT
                    if cell in ["ò"]:
                        orientation = SpikeOrientations.LEFT

                    spike = Spike(idy*SIZE, idx*SIZE,orientation=orientation)
                    self.servicelocator.actorList.append(spike)

                elif cell in POWERS:
                    if cell == "r":
                        dr = DashResetEntity(idy*SIZE, idx*SIZE, self.servicelocator)
                        self.servicelocator.actorList.append(dr)
                    if cell == "q":
                        s = Strawberry(idy*SIZE, idx*SIZE, self.servicelocator)
                        self.servicelocator.actorList.append(s)
                    if cell == "s":
                        sp = Spring(idy*SIZE, idx*SIZE, self.servicelocator)
                        self.servicelocator.actorList.append(sp)
                    if cell == "t":
                        fb = FallingBlock(idy*SIZE, idx*SIZE, self.servicelocator)
                        self.servicelocator.actorList.append(fb)
                        self.servicelocator.fallingBlocks.append(fb)
                    if cell == "u":
                        cd = Cloud(idy*SIZE, idx*SIZE,self.servicelocator) 
                        self.servicelocator.actorList.append(cd)
                        self.servicelocator.clouds.append(cd)
                    if cell == "v":
                        du = DashUpgrade(idy*SIZE, idx*SIZE)
                        self.servicelocator.actorList.append(du)

        return sprites, spawn, walls

    def draw(self, screen:pygame.display) -> None:
        """
        Draws the map

        Args:
            screen (pygame.display): display to draw the map on

        Returns:
            None
        
        """
        self.sprites.draw(screen)

