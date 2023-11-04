import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import StawberryStuff
from constants.enums import ActorTypes



class Strawberry(Actor):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.height = 80
        self.width = 80
        self.name = id(self)
        self.type = ActorTypes.STRAWBERRY

        #sprite e state
        self.state = "idle"
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.animationCounter = 0


    def update(self):
        if self.state != "hidden":
            if self.spriteID== "collected13":
                self.state = "hidden"
                return
            if self.animationCounter % 5 == 0:
                self.spriteID = StawberryStuff.sprites[self.spriteID]
            self.animationCounter += 1
            self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)

    def draw(self, display):
        if self.state != "hidden":
            self.sprite.draw(display)

    def notify(self, entityName, event):
        if event == "strawberryCollected" and entityName == self.name:
            if self.state == "idle":
                self.state = "collected"
                self.spriteID = "collected1"
                self.animationCounter = 1