import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import cloudDicts
from constants.enums import ActorTypes,EventType,States

class Cloud(Actor):
    def __init__(self ,x:int ,y:int ,serviceLocator) -> None:
        """
        Creates a cloud

        Args:
            x (int): x position of the cloud
            y (int): y position of the cloud
            serviceLocator (ServiceLocator): ServiceLocator object
        
        Returns:
            None
        """
        super().__init__(x,y+10,40,100,serviceLocator)

        self.name = id(self)
        self.type = ActorTypes.CLOUD
        self.state = States.IDLE
        #sprite e state
        self.state = States.IDLE
        self.spriteID = States.IDLE.value + "1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
        self.rect = self.sprite.rect

    def update(self):
        """
        Updates the cloud's position and sprite

        Args:
            None

        Returns:
            None
        """
        self.x -= 3 if self.x > -100 else -self.serviceLocator.display.get_width() - 100
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
        

    def draw(self, display:pygame.display) -> None:
        """
        Draws the cloud

        Args:
            display (pygame.display): display where the cloud is drawn

        Returns:
            None
        """
        self.sprite.draw(display)

    def notify(self, entityName:str, event:EventType) -> None:
        """
        Notifies the cloud of an event

        Args:
            entityName (str): name of the entity that triggered the event
            event (EventType): event triggered
    
        Returns:
            None
        """
        if event == "touchCloud" and entityName == self.name:
            pass
