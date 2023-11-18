import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import cloudStuff
from constants.enums import ActorTypes

class Cloud(Actor):
    def __init__(self, x, y,serviceLocator) -> None:
        super().__init__(x,y+10,40,100,serviceLocator)

        self.name = id(self)
        self.type = ActorTypes.CLOUD
        self.state = "idle"
        #sprite e state
        self.state = cloudStuff.states[0]
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
        self.rect = self.sprite.rect
        print("cloud created")

    def update(self):
        self.x -= 3 if self.x > -100 else -900
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
        

    def draw(self, display):
        self.sprite.draw(display)

    def notify(self, entityName, event):
        if event == "touchCloud" and entityName == self.name:
            pass
