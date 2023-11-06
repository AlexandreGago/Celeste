import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import StawberryStuff
from constants.enums import ActorTypes



class Spike(Actor):
    def __init__(self, x, y) -> None:
        super().__init__(x,y+20,30,50,None)

        self.name = id(self)
        self.type = ActorTypes.SPIKE

        #sprite e state
        self.state = "idle"
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)


    def update(self):
        pass

    def draw(self, display):
        if self.state != "hidden":
            self.sprite.draw(display)

    def notify(self, entityName, event):
        if event == "touchSpike" and entityName == self.name:
            pass