import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import fallingBlockStuff
from constants.enums import ActorTypes

class FallingBlock(Actor):
    def __init__(self, x, y,serviceLocator) -> None:
        super().__init__(x+5,y+35,15,45,serviceLocator)

        self.name = id(self)
        self.type = ActorTypes.FALLINGBLOCK
        self.state = "idle"
        #sprite e state
        self.state = fallingBlockStuff.states[0]
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
        self.rect = self.sprite.rect

        self.shake = 0
        self.shakeDir = "left"
        self.animationFrameCounter = 0

    def update(self):
        # print(self.state)
        if self.state == "falling":
            if self.animationFrameCounter % 5 == 0:
                self.shake += -2 if self.shakeDir == "left" else 2
                self.shakeDir = "left" if self.shake >= 2 else "right" if self.shake <= -2 else self.shakeDir
                self.sprite.update(self.x+self.shake,self.y,self.height,self.width,self.spriteID)
                self.rect = self.sprite.rect

            if self.animationFrameCounter == 100:
                self.state = "outline"
                self.spriteID = "outline1"
                self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
                self.animationFrameCounter = 0

        if self.state == "outline":
            if self.animationFrameCounter == 120:
                print("change to idle")
                self.state = "idle"
                self.spriteID = "idle1"
                self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
                self.animationFrameCounter = 0

        self.animationFrameCounter += 1
        

    def draw(self, display):
        self.sprite.draw(display)

    def notify(self, entityName, event):
        if event == "touchFallingBlock" and entityName == self.name:
            if self.state == "idle":
                self.state = "falling"
                self.spriteID = "falling1"
                self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
                self.animationFrameCounter = 0
            if self.state == "outline":
                self.animationFrameCounter = 0
