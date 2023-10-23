from actor import Actor
import pygame
from enums import ActorTypes
from dictionaries import PlayerStuff
from spriteClass import SpriteClass

import time

Y_GRAVITY = 9
MOVEMENT_X = 9

WIDTH, HEIGHT = 800, 800

JUMP_POWER = 200
JUMP_SPEED = 2

ANIMATION_SPEEDS = {
    "jump": 10,
    "turn": 2
}



#(offset_x,offset_y),max_dist,(pos_x,pos_y),radius
points = [
    [pygame.Vector2(0,0),0,pygame.Vector2(0,0),25], #first point is the center of the head
    [pygame.Vector2(-6,4),12,pygame.Vector2(0,0),23],
    [pygame.Vector2(-2,4),11,pygame.Vector2(0,0),22],
    [pygame.Vector2(-4,4),10.5,pygame.Vector2(0,0),21], 
    [pygame.Vector2(-4,2),10,pygame.Vector2(0,0),20],
    [pygame.Vector2(-2,2),9.5,pygame.Vector2(0,0),19],
]
class Player(Actor):
    def __init__(self,x,y,name,serviceLocator) -> None:
        """
        Player class
        
        Args:
            x (int): spawn x position
            y (int): spawn y position
            name (string): name of the player
            serviceLocator (ServiceLocator): service locator

        Returns:
            None

        """
        #call the parent constructor (Actor)
        super().__init__()

        self.name = name
        self.serviceLocator = serviceLocator

        #set the starting position
        self.x = x
        self.y = y

        self.type = ActorTypes.PLAYER

        #set the starting state (idle)
        self.state = PlayerStuff.states[0]
        #set the starting sprite (idle1)
        self.spriteID = f"{self.state}1"
        
        #this controls the jump
        self.jumpPower = 0
        #this controls the jump state
        self.jumpAux = "init"
        #set the starting orientation
        self.orientation = "right"

        #size of the sprite
        self.height = 80
        self.width = 70

        #auxiliar variable to control the animation
        self.animationFrameCounter = 0
        
        #create the sprite and update it
        sprite = SpriteClass(self.height,self.width,self.type,self.serviceLocator,self.spriteID)
        sprite.update(self.x,self.y,self.height,self.width,self.spriteID,self.orientation=="right")
        self.sprite = sprite
        

    def move(self, vector: tuple[int, int]) -> None:
        """
        Move the player
        
        A
        """
        vectorToState = {
            (0,0): "idle",
            (0,1): "crouch",
            (0,-1): "jump",
            (1,0): "walkRight",
            (-1,0): "walkLeft",
            (1,1): "crouch",
            (1,-1): "jump",
            (-1,1): "crouch",
            (-1,-1): "jump",
        }


        newState = vectorToState[vector]
        if self.state == "jump":
            #default jump state
            if self.jumpAux == "init":
                self.jumpAux = "up"
                self.jumpPower = JUMP_POWER
                self.animationFrameCounter = 0
                self.spriteID = "jump1"

            #move up while reducing the jump power
            elif self.jumpAux == "up":
                self.y -= JUMP_SPEED * Y_GRAVITY 
                #reduce jump power
                self.jumpPower -= Y_GRAVITY if self.jumpPower > 0 else 0
                if self.animationFrameCounter % 10 == 0:
                    if self.spriteID == "jump1":
                        self.spriteID = PlayerStuff.sprites[self.spriteID]
                    else:
                        self.spriteID = "jump1"

                #if jump power is 0, start falling
                if self.jumpPower <= 0:
                    self.jumpAux = "down"
                    self.jumpPower = 0
                    self.spriteID = PlayerStuff.sprites["jump2"]

    	    #we are falling
            elif self.jumpAux == "down":
                if self.animationFrameCounter % 15 == 0:
                    if self.spriteID == "jump3":
                        self.spriteID = PlayerStuff.sprites[self.spriteID]
                    else:
                        self.spriteID = "jump3"
            

        #turning left or right
        elif self.state in ["turningLeft","turningRight"]:
            #if its not the end of the animation, keep playing it
            if self.spriteID != "turningLeft8" and self.spriteID != "turningRight8":
                if self.animationFrameCounter % ANIMATION_SPEEDS["turn"] == 0:
                    self.spriteID = PlayerStuff.sprites[self.spriteID]
            #if its the end of the animation, change the state
            else:
                if self.state == "turningLeft":
                    self.state = "walkLeft"
                else:
                    self.state = "walkRight"

                self.spriteID = f"{self.state}1"
                self.animationFrameCounter = 0

        elif self.state in ["walkRight","walkLeft","crouch","idle"]:
            if newState != self.state:
                #turn left
                if self.orientation == "right" and newState == "walkLeft":
                    newState = "turningLeft"
                elif self.orientation == "left" and newState == "walkRight":
                    newState = "turningRight"
                self.state = newState
                self.spriteID = f"{newState}1"
                self.animationFrameCounter = 0

            else:
                if self.animationFrameCounter % 10 == 0:
                    self.spriteID = PlayerStuff.sprites[self.spriteID]




        #!The sprite rect still has the old position, so we need to update it first
        self.y += Y_GRAVITY
        self.sprite.rect.y = self.y

        for tile in self.serviceLocator.map.walls:
            if self.sprite.rect.colliderect(tile.rect):
                #ceiling
                if tile.rect.bottom - self.sprite.rect.top <= Y_GRAVITY:
                    # print("ceiling")
                    self.y = tile.rect.bottom
                #ground
                elif tile.rect.top - self.sprite.rect.bottom >= -1*Y_GRAVITY:
                    # print("ground")
                    self.y = tile.rect.top - self.height
                    if self.jumpAux == "down":
                        self.state = newState
                        self.jumpAux = "init"
                        self.spriteID = f"{newState}1"
                        self.animationFrameCounter = 0
                #update sprite rect
                self.sprite.rect.y = self.y

        #dont let the player go out of the screen
        if self.x + MOVEMENT_X*vector[0] < 0:
            self.x = 0
        elif self.x + vector[0] > WIDTH - self.width:
            self.x = WIDTH - self.width
        else:
            self.x += MOVEMENT_X*vector[0]

        #update sprite rect
        self.sprite.rect.x = self.x
        #left and right walls
        for tile in self.serviceLocator.map.walls:
            if self.sprite.rect.colliderect(tile.rect):
                #left wall
                if tile.rect.right - self.sprite.rect.left <= MOVEMENT_X:
                    # print("left wall")
                    self.x = tile.rect.right
                #right wall
                elif tile.rect.left - self.sprite.rect.right >= -1*MOVEMENT_X:
                    # print("right wall")
                    self.x = tile.rect.left - self.width
              
            
        #we don't have the mirrored sprites, so we just flip the sprite
        if self.state == "walkLeft" or self.state == "turningLeft":
            self.orientation = "left"
        elif self.state == "turningRight" or self.state == "walkRight":
            self.orientation = "right"
        #update sprite
        # print(self.spriteID)
        self.animationFrameCounter += 1
        # self.spriteGroup.update(self.x,self.y,self.height,self.width,self.spriteID,self.orientation=="left")
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID,self.orientation=="left")
        pygame.draw.rect(self.serviceLocator.display,(0,0,255),self.sprite.rect,1)

    #draws the hair
    def drawHair(self, display):
        #offset for the orientation of the character
        offsetDirX = PlayerStuff.spritesHairOffset[self.state][self.spriteID][0] + 9 if self.orientation == "right" else PlayerStuff.spritesHairOffset[self.state][self.spriteID][0]*-1 - 9
        offsetDirY = PlayerStuff.spritesHairOffset[self.state][self.spriteID][1] + 16
        for i in range (len(points)-1,-1,-1):
            if i == 0:
                points[i][2] = pygame.Vector2(int(self.x + self.width / 2 +offsetDirX), int(self.y + self.height / 2-offsetDirY))
                continue
            if self.orientation == "right":
                points[i][2] = points[i][0] + points[i-1][2] 
            else:
                points[i][2] =  points[i-1][2]+(points[i][0][0]*-1,points[i][0][1])

        for i in range(len(points)):
            if i == 0:
                continue
            if points[i][2].distance_to(points[i][0]+points[i-1][2]) > points[i][1]:
                dir = (points[i][2]-(points[i-1][2]+points[i][0])).normalize()
                offset = dir * points[i][1]
                points[i][2] = points[i-1][2] + points[i][0]+ offset
                
        
        for i in range (len(points)):

            pygame.draw.circle(display, (128, 0, 0), points[i][2], points[i][3])

    
    def draw(self,display):
        self.drawHair(display)
        # self.spriteGroup.draw(display)
        self.sprite.draw(display)

        