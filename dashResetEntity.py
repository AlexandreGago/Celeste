import pygame
from actor import Actor
from enums import ActorTypes
from spriteClass import SpriteClass
from dictionaries import DashResetEntityStuff

class DashResetEntity(Actor):

    def __init__(self,x,y) -> None:
        super().__init__()
        self.type = ActorTypes.DASH_RESET
        self.x = x
        self.y = y
        self.width = 80
        self.height = 80
        self.name = id(self)

        self.state = "idle"
        self.animationCounter = 0
        self.disabledCounter = 0

        self.spriteID =  "idle1"
        self.sprite = SpriteClass(self.height,self.width,self.type,self.spriteID)

    def update(self):
        if self.state == "outline":
            if self.disabledCounter >= 300: # refill animation
                self.state = "refill"
                self.spriteID = "flash1"
                self.disabledCounter = 0
                self.animationCounter = 0
            else:
                self.disabledCounter += 1

        elif self.state == "refill":
            if self.animationCounter % 5 == 0:
                self.spriteID = DashResetEntityStuff.sprites[self.spriteID]
            if self.spriteID == "idle1":
                self.state = "idle"
                self.spriteID = "idle1"
                self.animationCounter = 0

        elif self.animationCounter % 5 == 0:
            self.spriteID = DashResetEntityStuff.sprites[self.spriteID]

        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
        self.animationCounter += 1
        

    def draw(self,display):
        self.sprite.draw(display)
    
    def notify(self, entityName, event):
        if event == "dashReset" and entityName == self.name:
            self.state = "outline"
            self.spriteID = "outline1"
            self.animationCounter = 1
            self.disabledCounter = 0

        if event == "ground" and self.state == "outline":
            self.state = "refill"
            self.spriteID = "flash1"
            self.animationCounter = 0
