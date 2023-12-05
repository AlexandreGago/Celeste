import pygame
from actors.actor import Actor
from constants.enums import ActorTypes,EventType,States
from spriteClass import SpriteClass
from constants.dictionaries import DashResetDicts

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
        super().__init__(x,y,50,50,serviceLocator)
        self.type = ActorTypes.DASH_RESET
        self.name = id(self)

        self.state = States.IDLE
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
        if self.state == States.OUTLINE:
            if self.disabledCounter >= 300: # refill animation
                self.state = States.REFILL
                self.spriteID = "flash1"
                self.disabledCounter = 0
                self.animationCounter = 0
                self.serviceLocator.soundManager.play("dashEntityReset")
            else:
                self.disabledCounter += 1

        elif self.state == States.REFILL:
            if self.animationCounter % 5 == 0:
                self.spriteID = DashResetDicts.sprites[self.spriteID]
            if self.spriteID == "idle1":
                self.state = States.IDLE
                self.spriteID = "idle1"
                self.animationCounter = 0
                #play refresh sound

                

        elif self.animationCounter % 5 == 0:
            self.spriteID = DashResetDicts.sprites[self.spriteID]

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
    
    def notify(self, entityName:str, event:EventType)->None:
        """
        Notifies the entity of an event

        Args:
            entityName (str): name of the entity that triggered the event
            event (EventType): event triggered

        Returns:
            None
        """
        if event == EventType.DASH_RESET_COLLISION and entityName == self.name:
            self.state = States.OUTLINE
            self.spriteID = "outline1"
            self.animationCounter = 1
            self.disabledCounter = 0
            self.serviceLocator.soundManager.play("dashEntityBreak")

        if (event == EventType.GROUND_COLLISION or event == EventType.SPRING_COLLISION) and self.state == States.OUTLINE:
            self.state = States.REFILL
            self.spriteID = "flash1"
            self.animationCounter = 0
            self.serviceLocator.soundManager.play("dashEntityReset")      
   