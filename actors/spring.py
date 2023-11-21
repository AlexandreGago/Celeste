import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import SpringStuff
from constants.enums import ActorTypes



class Spring(Actor):
    def __init__(self, x:int, y:int, serviceLocator) -> None:
        """
        Creates a spring

        Args:
            x (int): x position of the spring
            y (int): y position of the spring
            serviceLocator (ServiceLocator): ServiceLocator object

        Returns:
            None
        """
        super().__init__(x,y,50,45,serviceLocator)
        self.name = id(self)
        self.type = ActorTypes.SPRING

        #sprite e state
        self.state = "idle"
        self.spriteID = "idle1"

        
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        
        self.animationCounter = 0


    def update(self) -> None:
        """
        Updates the spring's sprite and state

        Args:
            None

        Returns:
            None

        """
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

    def draw(self, display:pygame.display) -> None:
        """
        Draws the spring on the display

        Args:
            display (pygame.display): pygame display

        Returns:
            None

        """
        self.sprite.draw(display)
        # pygame.draw.rect(display,(0,0,255),self.sprite.rect,1)


    def notify(self, entityName:str, event:str) -> None:
        """
        Notifies the spring of an event

        Args:
            entityName (str): name of the entity that triggered the event
            event (str): event triggered

        Returns:
            None
        """
        if event == "springCollision" and entityName == self.name:
            if self.state == "idle":
                self.serviceLocator.soundManager.play("spring")
                self.state = "extended"
                self.spriteID = "extended1"
                self.animationCounter = 1