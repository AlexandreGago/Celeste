import pygame, random
from constants.dictionaries import jumpParticles
from constants.enums import ParticleTypes
from spriteClass import SpriteClass
# a particle is...
# a thing that exists at a location
# typically moves around
# typically changes over time
# and typically disappears after a certain amount of time

# [loc, velocity, timer]
class SpriteParticle:
    def __init__(self,x,y,action) -> None:
        self.x = x
        self.y = y
        self.action = action
        if action == "jump":
            self.type = ParticleTypes.JUMP
        else:
            self.type = None
            
        self.timer = 27
        self.velocity = [-1,0.1]#[random.randint(0, 20) / 10 - 1, -2]
        self.size = random.randint(30, 30)
        self.color = (255, 255, 255)
        
        self.spriteID = jumpParticles.firstSprite
        self.sprite = SpriteClass(self.x,self.y,self.size,self.size,self.type,self.spriteID)
        self.animationCounter = 1
    
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.timer -= 1
        self.velocity[0] -= 0.1
        self.color = (255, 255, 255)
        
        if self.animationCounter % 10 == 0:
            self.spriteID = jumpParticles.sprites[self.spriteID]
            self.animationCounter = 1
        #update sprite
        self.sprite.update(self.x,self.y,self.size,self.size,self.spriteID)
        self.animationCounter += 1
        
        if self.timer <= 0:
            return True
        return False
    
    def draw(self,display):
        self.sprite.draw(display)
        

