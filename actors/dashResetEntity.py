import pygame
from actors.actor import Actor
from constants.enums import ActorTypes
from spriteClass import SpriteClass
from constants.dictionaries import DashResetEntityStuff

class DashResetEntity(Actor):

    def __init__(self,x:int,y:int, serviceLocator) -> None:
        """
        Creates a dash reset entity

        Args:
            x (int): x position of the entity
            y (int): y position of the entity
            serviceLocator (ServiceLocator): ServiceLocator object

        Returns:
            None

        """
        super().__init__(x,y,80,80,serviceLocator)
        self.type = ActorTypes.DASH_RESET
        self.name = id(self)

        self.state = "idle"
        self.animationCounter = 0
        self.disabledCounter = 0

        self.serviceLocator = serviceLocator

        self.spriteID =  "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)

    def update(self)->None:
        """
        Updates the entity's position ,sprite and state

        Args:
            None

        Returns:
            None

        """
        if self.state == "outline":
            if self.disabledCounter >= 300: # refill animation
                self.state = "refill"
                self.spriteID = "flash1"
                self.disabledCounter = 0
                self.animationCounter = 0
                self.serviceLocator.soundManager.play("dashEntityReset")
            else:
                self.disabledCounter += 1

        elif self.state == "refill":
            if self.animationCounter % 5 == 0:
                self.spriteID = DashResetEntityStuff.sprites[self.spriteID]
            if self.spriteID == "idle1":
                self.state = "idle"
                self.spriteID = "idle1"
                self.animationCounter = 0
                #play refresh sound

                

        elif self.animationCounter % 5 == 0:
            self.spriteID = DashResetEntityStuff.sprites[self.spriteID]

        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
        self.animationCounter += 1
        

    def draw(self,display:pygame.display):
        """
        Draws the entity

        Args:
            display (pygame.display): display where the entity is drawn

        Returns:
            None
        """
        self.sprite.draw(display)
    
    def notify(self, entityName:str, event:str)->None:
        """
        Notifies the entity of an event

        Args:
            entityName (str): name of the entity that triggered the event
            event (str): event triggered

        Returns:
            None
        """
        if event == "dashReset" and entityName == self.name:
            self.state = "outline"
            self.spriteID = "outline1"
            self.animationCounter = 1
            self.disabledCounter = 0
            self.serviceLocator.soundManager.play("dashEntityBreak")

        if event == "ground" and self.state == "outline":
            self.state = "refill"
            self.spriteID = "flash1"
            self.animationCounter = 0
            self.serviceLocator.soundManager.play("dashEntityReset")      

        if event == "springCollision" and self.state == "outline":
            self.state = "refill"
            self.spriteID = "flash1"
            self.animationCounter = 0
            self.serviceLocator.soundManager.play("dashEntityReset")      