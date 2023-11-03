import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import SpringStuff
from constants.enums import ActorTypes



class Spring(Actor):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.height = 50
        self.width = 45
        self.name = id(self)
        self.type = ActorTypes.SPRING

        #sprite e state
        self.state = "idle"
        self.spriteID = "idle1"

        
        self.sprite = SpriteClass(self.height,self.width,self.type,self.spriteID)
        
        self.animationCounter = 0


    def update(self):
        if self.state == "extended" and self.spriteID == "extended5":
            self.state = "idle"
            self.spriteID = "idle1"
            self.animationCounter = 1

            
        if self.animationCounter % 5 == 0:
            self.spriteID = SpringStuff.sprites[self.spriteID]
            
        self.animationCounter += 1
        
        spriteX = self.x + SpringStuff.spritesOffset[self.spriteID][0]
        spriteY = self.y + SpringStuff.spritesOffset[self.spriteID][1]
        spriteHeight = self.height - SpringStuff.spritesOffset[self.spriteID][1]
        spriteWidth = self.width - SpringStuff.spritesOffset[self.spriteID][0]
        
        self.sprite.update(spriteX,spriteY,spriteHeight,spriteWidth,self.spriteID)

    def draw(self, display):
        self.sprite.draw(display)
        pygame.draw.rect(display,(0,0,255),self.sprite.rect,1)


    def notify(self, entityName, event):
        if event == "springCollision" and entityName == self.name:
            if self.state == "idle":
                self.state = "extended"
                self.spriteID = "extended1"
                self.animationCounter = 1