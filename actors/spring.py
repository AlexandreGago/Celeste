import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import SpringDicts
from constants.enums import ActorTypes,EventType,States



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
        self.state = States.IDLE
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
        if self.state == States.EXTENDED and self.spriteID == "extended5": # if the spring is extended and the animation is finished, go back to idle
            self.state = States.IDLE
            self.spriteID = "idle1"
            self.animationCounter = 1

            
        if self.animationCounter % 5 == 0:# animation every 5 frames
            self.spriteID = SpringDicts.sprites[self.spriteID]
            
        self.animationCounter += 1
        
        #this is needed because the sprite is not centered
        spriteX = self.x + SpringDicts.spritesOffset[self.spriteID][0]
        spriteY = self.y + SpringDicts.spritesOffset[self.spriteID][1]
        spriteHeight = self.height - SpringDicts.spritesOffset[self.spriteID][1]
        spriteWidth = self.width - SpringDicts.spritesOffset[self.spriteID][0]
        
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


    def notify(self, entityName:str, event:EventType) -> None:
        """
        Notifies the spring of an event

        Args:
            entityName (str): name of the entity that triggered the event
            event (EventType): type of event

        Returns:
            None
        """
        if event == EventType.SPRING_COLLISION and entityName == self.name: # if the spring was collided with , change state to extended and play the spring sound
            if self.state == States.IDLE:
                self.serviceLocator.soundManager.play("spring")
                self.state = States.EXTENDED
                self.spriteID = "extended1"
                self.animationCounter = 1