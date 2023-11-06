import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import SpikeStuff
from constants.enums import ActorTypes,SpikeOrientations



class Spike(Actor):
    def __init__(self, x, y,orientation) -> None:
        xOffset = None
        yOffset = None
        rotateSprite = 0
        if orientation == SpikeOrientations.UP:
            xOffset = x + 5
            yOffset = y + 40
            self.width = 40
            self.height = 10

        if orientation == SpikeOrientations.LEFT:
            xOffset = x + 40
            yOffset = y + 5
            self.width = 10
            self.height = 40
            rotateSprite = 90

        if orientation == SpikeOrientations.DOWN:
            xOffset = x + 5
            yOffset = y
            self.width = 40
            self.height = 10
            rotateSprite = 180
        
        if orientation == SpikeOrientations.RIGHT:
            xOffset = x
            yOffset = y + 5
            self.width = 10
            self.height = 40
            rotateSprite = -90
            
        super().__init__(xOffset,yOffset,self.height,self.width,None)

        self.name = id(self)
        self.type = ActorTypes.SPIKE

        #sprite e state
        self.state = "idle"
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID,rotate = rotateSprite)


    def update(self):
        pass

    def draw(self, display):
        if self.state != "hidden":
            self.sprite.draw(display)

    def notify(self, entityName, event):
        if event == "touchSpike" and entityName == self.name:
            pass