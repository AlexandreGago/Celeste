from actor import Actor
import pygame
from enums import ActorTypes
from dictionaries import PlayerStuff
from spriteClass import SpriteClass

Y_GRAVITY = 2
MOVEMENT_X = 5

JUMP_POWER = 100
JUMP_SPEED = 10

ANIMATION_SPEEDS = {
    "jump": 10,
    "turn": 2
}

points = [
    [pygame.Vector2(0,0),0,pygame.Vector2(0,0),25], #first point is the center of the head
    [pygame.Vector2(-6,4),12,pygame.Vector2(0,0),23],
    [pygame.Vector2(-4,4),11,pygame.Vector2(0,0),22],
    [pygame.Vector2(-2,2),10.5,pygame.Vector2(0,0),21], 
    [pygame.Vector2(-2,2),10,pygame.Vector2(0,0),20],
    [pygame.Vector2(-2,2),9.5,pygame.Vector2(0,0),19],
    [pygame.Vector2(-2,2),9,pygame.Vector2(0,0),18],
    [pygame.Vector2(-2,2),8.5,pygame.Vector2(0,0),17],
    [pygame.Vector2(-2,2),8,pygame.Vector2(0,0),16],
]
class Player(Actor):
    def __init__(self,x,y,name,serviceLocator) -> None:
        super().__init__()
        self.name = name
        self.type = ActorTypes.PLAYER
        self.x = x
        self.y = y
        self.state = PlayerStuff.states[0]
        self.serviceLocator = serviceLocator
        self.spriteID = f"{self.state}1"
        self.jumpPower = 0
        self.orientation = "right"
        self.jumpAux = "init"

        self.height = 80
        self.width = 70

        self.animationFrameCounter = 0

        self.spriteGroup = pygame.sprite.Group()
        sprite = SpriteClass(self.height,self.width,self.type,self.serviceLocator,self.spriteID)
        self.spriteGroup.add(sprite)
    
    def move(self,newState):

        if self.state == "jump":
            #default jump state
            if self.jumpAux == "init":
                self.jumpAux = "up"
                self.jumpPower = JUMP_POWER
                self.animationFrameCounter = 0

            #move up while reducing the jump power
            elif self.jumpAux == "up":
                self.y -= JUMP_SPEED
                #reduce jump power
                self.jumpPower -= Y_GRAVITY if self.jumpPower > 0 else 0

                #if jump power is 0, start falling
                if self.jumpPower == 0:
                    self.jumpAux = "down"
                    self.spriteID == PlayerStuff.sprites["jump2"]

    	    #we are falling
            elif self.jumpAux == "down":
                #add gravity
                self.y += Y_GRAVITY
            
            #update sprite every x frames
            if self.animationFrameCounter % ANIMATION_SPEEDS["jump"] == 0:
                #jump1 -> jump2 ... jump4 -> jump1
                self.spriteID = PlayerStuff.sprites[self.spriteID]


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
                self.serviceLocator.frameCount = 0

            else:
                if self.animationFrameCounter % 10 == 0:
                    self.spriteID = PlayerStuff.sprites[self.spriteID]


        #         #ground
        # if (self.x//50*50,self.y // 50 * 50) in self.serviceLocator.map.collision_map:

        #     self.jumpAux = "init"
        #     self.state = newState
        #     self.spriteID = f"{newState}1"
        #     self.serviceLocator.frameCount = 0
        self.x += MOVEMENT_X*PlayerStuff.statesMovement[newState][0]
        if (self.x//50*50,self.y // 50 * 50) not in self.serviceLocator.map.collision_map:
            self.y += Y_GRAVITY
            
        #we don't have the mirrored sprites, so we just flip the sprite
        if self.state == "walkLeft" or self.state == "turningLeft":
            self.orientation = "left"
        elif self.state == "turningRight" or self.state == "walkRight":
            self.orientation = "right"
        #update sprite

        self.animationFrameCounter += 1

        self.spriteGroup.update(self.x,self.y,self.height,self.width,self.spriteID,self.orientation=="left")
        self.drawHair(self.serviceLocator.getDisplay())
    #draws the hair
    def drawHair(self, display):
        #offset for the orientation of the character
        offsetDirX = 6 if self.orientation == "right" else -6
        for i in range (len(points)-1,-1,-1):
            if i == 0:
                points[i][2] = pygame.Vector2(int(self.x + self.width / 2+offsetDirX), int(self.y + self.height / 2-16))
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
        self.spriteGroup.draw(display)

        