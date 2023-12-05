import pygame, random
from constants.dictionaries import jumpParticles
from constants.enums import ParticleTypes
from spriteClass import SpriteClass


class SpriteParticle:
    """
    Creates a sprite for a particle
    """
    def __init__(self,x,y,action) -> None:
        """
        Creates a sprite particle

        Args:
            x (int): x position of the particle
            y (int): y position of the particle
            action (str): action of the particle

        Returns:
            None
        """
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
        """
        Updates the particle position and sprite

        Args:
            None

        Returns:
            bool: True if the particle is dead, False otherwise
        """
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
    
    def draw(self,display:pygame.display):
        """
        Draws the particle

        Args:
            display (pygame.display): display where the particle is drawn

        Returns:
            None
        """
        self.sprite.draw(display)
        

