import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import SpikeStuff
from constants.enums import ActorTypes,SpikeOrientations



class DashUpgrade(Actor):
    def __init__(self, x:int, y:int) -> None:

        self.height = 50
        self.width = 50
            
        super().__init__(x,y,self.height,self.width,None)

        self.name = id(self)
        self.type = ActorTypes.DASH_UPGRADE


        #sprite e state
        self.state = "idle"
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)

        self.yOffset = 0
        self.offsetDir = "down"

    def update(self):
        if self.state == "idle":
            if self.offsetDir == "down":
                self.yOffset += 0.2
                if self.yOffset >= 5:
                    self.offsetDir = "up"
            else:
                self.yOffset -= 0.2
                if self.yOffset <= -5:
                    self.offsetDir = "down"
            self.sprite.update(self.x,self.y+self.yOffset,self.height,self.width,self.spriteID)

    def draw(self, display:pygame.display) -> None:
        if self.state != "hidden":
            self.sprite.draw(display)

    def notify(self, entityName, event) -> None:
        if event == "touchDashUpgrade" and entityName == self.name and self.state =="idle":
            self.state = "hidden"