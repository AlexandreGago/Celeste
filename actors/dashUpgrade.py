import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.enums import ActorTypes,EventType,States



class DashUpgrade(Actor):
    def __init__(self, x:int, y:int,serviceLocator) -> None:
        """
            Creates the dash upgrade (when the player collects it, it gains more dashes)

            Args:
                x (int): x position of the dash upgrade
                y (int): y position of the dash upgrade
                serviceLocator (ServiceLocator): ServiceLocator object

            Returns:
                None
        """

        self.height = 50
        self.width = 50
            
        super().__init__(x,y,self.height,self.width,None)

        self.name = id(self)
        self.type = ActorTypes.DASH_UPGRADE

        self.serviceLocator = serviceLocator

        #sprite e state
        self.state = States.IDLE
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)

        self.yOffset = 0
        self.offsetDir = "down"

    def update(self):
        """
            Updates the dash upgrade's position and sprite

            Args:
                None

            Returns:
                None
        """
        if self.state == States.IDLE:
            if self.offsetDir == "down":# wiggle
                self.yOffset += 0.2
                if self.yOffset >= 5:
                    self.offsetDir = "up"
            else:# wiggle
                self.yOffset -= 0.2
                if self.yOffset <= -5:
                    self.offsetDir = "down"
            self.sprite.update(self.x,self.y+self.yOffset,self.height,self.width,self.spriteID)

    def draw(self, display:pygame.display) -> None:
        """
            Draws the dash upgrade

            Args:
                display (pygame.display): display where the dash upgrade is drawn

            Returns:
                None
        """
        if self.state != States.HIDDEN: # if not hidden, draw
            self.sprite.draw(display)

    def notify(self, entityName:str, event:EventType) -> None:
        """
            Notifies the dash upgrade of an event

            Args:
                entityName (str): name of the entity that triggered the event
                event (EventType): event triggered
        
            Returns:
                None
        """
        if event == EventType.DASH_UPGRADE_COLLISION and entityName == self.name and self.state ==States.IDLE: # if player collides with it
            self.state =  States.HIDDEN
            self.serviceLocator.soundManager.play("dashUpgrade",volume=0.5)
            