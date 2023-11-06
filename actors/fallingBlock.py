import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import fallingBlockStuff
from constants.enums import ActorTypes

class FallingBlock(Actor):
    def __init__(self, x, y,serviceLocator) -> None:
        super().__init__(x,y+35,15,50,serviceLocator)

        self.name = id(self)
        self.type = ActorTypes.FALLINGBLOCK
        self.state = "idle"
        #sprite e state
        self.state = fallingBlockStuff.states[0]
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
        self.rect = self.sprite.rect

    def update(self):
        pass

    def draw(self, display):
        self.sprite.draw(display)

    def notify(self, entityName, event):
        if event == "touchFallingBlock" and entityName == self.name:
            if self.state == "idle":
                self.state = "outline"
                self.spriteID = "outline1"
                self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
