import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import StawberryDicts
from constants.enums import ActorTypes,EventType,States



class Strawberry(Actor):
    def __init__(self, x:int, y:int, serviceLocator) -> None:
        """
        Creates a strawberry

        Args:
            x (int): x position of the strawberry
            y (int): y position of the strawberry
            serviceLocator (ServiceLocator): ServiceLocator object

        Returns:
            None
        """
        super().__init__(x,y,50,50,serviceLocator)

        self.name = id(self)
        self.type = ActorTypes.STRAWBERRY

        #sprite e state
        self.state = States.IDLE
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.animationCounter = 0


    def update(self) -> None:
        """
        Updates the strawberry's sprite and state

        Args:
            None

        Returns:
            None

        """
        if self.state != States.HIDDEN:
            if self.spriteID== "collected13":
                self.state = States.HIDDEN
                return
            if self.animationCounter % 5 == 0:
                self.spriteID = StawberryDicts.sprites[self.spriteID]
            self.animationCounter += 1
            self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)

    def draw(self, display:pygame.display) -> None:
        """
        Draws the strawberry

        Args:
            display (pygame.display): pygame.display object

        Returns:
            None

        """
        if self.state != States.HIDDEN:
            self.sprite.draw(display)

    def notify(self, entityName:str, event:EventType) -> None:
        """
        Notifies the strawberry of an event

        Args:
            entityName (str): name of the entity that triggered the event
            event (EventType): type of event

        Returns:
            None
            
        """
        if event == EventType.STRAWBERRY_COLLISION and entityName == self.name:
            if self.state == States.IDLE:
                self.serviceLocator.soundManager.play("strawberry")
                self.state = States.COLLECTED
                self.spriteID = "collected1"
                self.animationCounter = 1
                self.serviceLocator.score += 1000