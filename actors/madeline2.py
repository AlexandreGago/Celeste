from actors.actor import Actor
import pygame
import pygame.gfxdraw
from constants.enums import ActorTypes,PlayerStates,PlayerJumpStates,PlayerOrientation
from constants.dictionaries import PlayerStuff
from spriteClass import SpriteClass
from states import *
import utils.utils as utils
import math
from actors.spriteParticle import SpriteParticle

import time


Y_GRAVITY = 8
MOVEMENT_X = 5

WIDTH, HEIGHT = 800, 800

JUMP_SPEED = 6
COYOTE_COUNTER = 10
JUMP_RESET = 10
JUMP_REFRESH_TIMER = 1
JUMP_DURATION = 14
JUMP_SLOW_DURATION = 10
JUMP_SPRING_DURATION = 2*JUMP_DURATION
SPRING_COLLISION_COOLDOWN = 60

DASH_SPEED = 10
DASH_DURATION = 10
DASH_SLOW_UP_DURATION = 10
DASH_SLOW_DOWN_DURATION = 10
DASH_REFRESH_TIMER = 0


ANIMATION_SPEEDS = {
    "jump": 10,
    "turn": 2,
    "dash" : 1
}




#(offset_x,offset_y),max_dist,(pos_x,pos_y),radius
points = [
    [pygame.Vector2(0,0),0,pygame.Vector2(0,0),15], #first point is the center of the head
    [pygame.Vector2(-6,4),9,pygame.Vector2(0,0),14],
    [pygame.Vector2(-2,4),8.5,pygame.Vector2(0,0),13],
    [pygame.Vector2(-4,4),8,pygame.Vector2(0,0),12], 
    [pygame.Vector2(-4,2),7.5,pygame.Vector2(0,0),11],
    [pygame.Vector2(-2,2),7,pygame.Vector2(0,0),10],
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
        self.spawnX = x
        self.y = 800
        self.spawnHeight = y
        
        self.alive = False
        self.type = ActorTypes.PLAYER
        self.enableCollision = False

        #set the starting state (idle)
        self.state = PlayerStates.RESPAWN
        #set the starting sprite (idle1)
        self.spriteID = f"{self.state.value}1"
        
        #variable that holds grounded value of last frame
        self.wasGrounded = False
        self.jumped = False
        self.coyoteCounter = 0
        self.jumpRefreshTimer = 0
        
        #this controls the jump state
        self.jumpState = PlayerJumpStates.INIT
        #this controls the duration of the jump (up)
        self.jumpDuration = 0
        self.jumpSlowDuration = 0
        #spring
        self.springCollided = False
        self.springCollsionCooldown = SPRING_COLLISION_COOLDOWN
        #set the starting orientation
        self.orientation = PlayerOrientation.RIGHT

        #size of the sprite
        self.height = 50
        self.width = 50

        #auxiliar variable to control the animation
        self.animationFrameCounter = 0
        
        #create the sprite and update it
        sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        sprite.update(self.x,self.y,self.height,self.width,self.spriteID,self.orientation==PlayerOrientation.RIGHT)
        self.sprite = sprite

        self.dashCount = 1
        self.dashFrameCounter = 0
        self.dashRefreshTimer = 0
        self.dashDirection = [0,0]
        self.dashState = "end"
        
        self.particles = []
        
        return
    
    def spawn(self):
        if self.y > self.spawnHeight:    
            self.y -= 8
        else:
            return True
        return False
             
    def respawn(self):
        self.alive = self.spawn()
        if self.alive:
            self.state = PlayerStates.IDLE
            self.spriteID = f"{self.state.value}1"
            self.animationFrameCounter = 0
            self.enableCollision = True

    def jump(self):
        #default jump state
        if self.springCollided ==True:
            self.jumpState = PlayerJumpStates.UP
            self.animationFrameCounter = 0
            self.jumpDuration = JUMP_SPRING_DURATION
            self.spriteID = "jump1"
            self.jumpRefreshTimer = JUMP_REFRESH_TIMER
            self.springCollided = False
            self.dashCount = 1
            self.jumped = True

        elif self.jumpState == PlayerJumpStates.INIT:
            self.jumpState = PlayerJumpStates.UP
            self.animationFrameCounter = 0
            self.jumpDuration = JUMP_DURATION
            self.spriteID = "jump1"
            self.jumpRefreshTimer = JUMP_REFRESH_TIMER
            self.jumped = True
            #play jump sound
            #self.playSound("jump",1)
            self.serviceLocator.soundManager.play("jump")

            #create jump particle
            self.particles.append(SpriteParticle(self.x + self.width/2,self.y + self.height/2,"jump"))

        #move up while reducing the jump power
        elif self.jumpState == PlayerJumpStates.UP:
            self.y -= Y_GRAVITY + JUMP_SPEED
            self.jumpDuration -= 1 if self.jumpDuration > 0 else 0
            #reduce jump power
            if self.animationFrameCounter % 10 == 0:
                if self.spriteID == "jump1":
                    self.spriteID = PlayerStuff.sprites[self.spriteID]
                else:
                    self.spriteID = "jump1"

            #if jumpDuration is 0, start falling
            if self.jumpDuration <= 0:
                self.jumpState = PlayerJumpStates.SLOWUP
                self.jumpSlowDuration = JUMP_SLOW_DURATION

        elif self.jumpState == PlayerJumpStates.SLOWUP:
            self.y -= Y_GRAVITY + JUMP_SPEED/2
            if self.animationFrameCounter % 10 == 0:
                self.spriteID = PlayerStuff.sprites[self.spriteID]
                
            self.jumpSlowDuration -= 1 if self.jumpSlowDuration > 0 else 0
            if self.jumpSlowDuration <= 0:
                self.jumpState = PlayerJumpStates.SLOWDOWN
                self.jumpSlowDuration = JUMP_SLOW_DURATION
                self.spriteID = PlayerStuff.sprites["jump2"]

        elif self.jumpState == PlayerJumpStates.SLOWDOWN:
            self.y -= Y_GRAVITY - JUMP_SPEED/2
            if self.animationFrameCounter % 15 == 0:
                self.spriteID = PlayerStuff.sprites[self.spriteID]

            self.jumpSlowDuration -= 1 if self.jumpSlowDuration > 0 else 0
            if self.jumpSlowDuration <= 0:
                self.jumpState = PlayerJumpStates.DOWN
                self.spriteID = PlayerStuff.sprites["jump3"]

        #we are falling
        elif self.jumpState == PlayerJumpStates.DOWN:
            if self.animationFrameCounter % 15 == 0:
                if self.spriteID == "jump3":
                    self.spriteID = PlayerStuff.sprites[self.spriteID]
                else:
                    self.spriteID = "jump3"
    
    
    def dash(self):
        print(self.dashState,self.dashFrameCounter,self.dashDirection,self.orientation)
        if self.dashState == "fast":
            if self.dashDirection[0] != 0:
                self.x += DASH_SPEED if self.orientation == PlayerOrientation.RIGHT else -1 *DASH_SPEED
            #looking up dash
            if self.dashDirection[1] != 0:
                self.y -= DASH_SPEED if self.dashDirection[1] == 1 else -1*DASH_SPEED
            
            #during the dash, we are not affected by gravity
            self.y -= Y_GRAVITY

            if self.animationFrameCounter % ANIMATION_SPEEDS["dash"] == 0:
                self.spriteID = PlayerStuff.sprites[self.spriteID]
            if self.dashFrameCounter >= DASH_DURATION:
                if self.dashDirection[1] != 1:
                    self.dashState = "slowDown"
                    self.dashFrameCounter+=DASH_SLOW_UP_DURATION
                else:
                    self.dashState = "slowUp"


        elif self.dashState == "slowUp":

            if self.dashDirection[1] == 1:
                self.y -= DASH_SPEED/2
            else:
                self.y += DASH_SPEED/2
            #during the dash, we are not affected by gravity
            self.y -= Y_GRAVITY

            if self.animationFrameCounter % ANIMATION_SPEEDS["dash"] == 0:
                self.spriteID = PlayerStuff.sprites[self.spriteID]
            if self.dashFrameCounter >= DASH_DURATION + DASH_SLOW_UP_DURATION:
                self.dashState = "slowDown"

        elif self.dashState == "slowDown":
            # if self.dashDirection[0] != 0:
            #     self.x += DASH_SPEED/2 if self.orientation == PlayerOrientation.RIGHT else -1 *DASH_SPEED/2
            self.y += DASH_SPEED/2
            #during the dash, we are not affected by gravity
            self.y -= Y_GRAVITY

            if self.animationFrameCounter % ANIMATION_SPEEDS["dash"] == 0:
                self.spriteID = PlayerStuff.sprites[self.spriteID]


        self.dashFrameCounter += 1


    def turn(self):
        if self.animationFrameCounter % ANIMATION_SPEEDS["turn"] == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]
            
    def idle(self):
        if self.animationFrameCounter % 10 == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]

    def walk(self):
        if self.animationFrameCounter % 10 == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]

    def crouch(self):
        if self.animationFrameCounter % 10 == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]
   
    
    def newstate(self, vector):
        """
        decide newstate based on vector and state variables
        """
        xInput,yInput,dashInput,upInput = vector

        newState = PlayerStuff.vectorToState[(xInput,yInput)]
        #reduce coyotejump counter
        self.coyoteCounter -= 1 if self.coyoteCounter > 0 else 0
        #reduce spring collision cooldown
        self.springCollsionCooldown -= 1 if self.springCollsionCooldown > 0 else 0
        
        #if we were grounded last frame, reduce the jump cooldown and the dash cooldown
        if self.wasGrounded:
            self.dashRefreshTimer -= 1 if self.dashRefreshTimer > 0 else 0
            self.jumpRefreshTimer -= 1 if self.jumpRefreshTimer > 0 else 0

        if self.alive == False:
            newState = PlayerStates.RESPAWN
            self.enableCollision = False
            
        #if last frame we collided with a spring, enter jump state
        elif self.springCollided:
            newState = PlayerStates.JUMP     
            for obs in self.observers:
                obs.notify(self.name,"ground")       

                
        #let dash if we have dashes and we are not dashing and cooldown is over
        elif dashInput >= 1 and self.dashCount > 0 and self.dashState != "fast" and self.dashRefreshTimer == 0:
            self.serviceLocator.offset = utils.screen_shake(5,15,4)
            self.dashCount -= 1
            self.dashRefreshTimer = DASH_REFRESH_TIMER
            newState = PlayerStates.DASH
            self.dashFrameCounter = 0
            self.dashState = "fast"
            #self.playSound("dash",1)
            self.serviceLocator.soundManager.play("dash")
            #!Avoid the real problem
            verticalDirection = 1 if upInput == 1 else -yInput if yInput != 0 else 0
            #change orientation and save the dash direction
            if xInput != 0:
                self.orientation = PlayerOrientation.LEFT if xInput < 0 else PlayerOrientation.RIGHT
                self.dashDirection = [xInput,verticalDirection]
            else:
                if verticalDirection != 0:
                    self.dashDirection = [0,verticalDirection]
                else:
                    self.dashDirection = [1,verticalDirection] if self.orientation == PlayerOrientation.RIGHT else [-1,verticalDirection]


        #if we collide with a spring or pressed jump, enter jump state
        elif newState == PlayerStates.JUMP:
            #if we are grounded and we are not jumping and we still can jump and cooldown is over
            if self.state != PlayerStates.JUMP and self.coyoteCounter > 0 and self.jumpRefreshTimer <= 0 and self.wasGrounded:
                newState = PlayerStates.JUMP
                self.jumpState = PlayerJumpStates.INIT 
            else:
                #keep the same state
                newState = self.state  

        elif self.orientation == PlayerOrientation.RIGHT and xInput <= -1:
            newState = PlayerStates.TURN
        elif self.orientation == PlayerOrientation.LEFT  and xInput >= 1:
            newState = PlayerStates.TURN
        
        if self.state == PlayerStates.RESPAWN:
            if self.alive == True:
                newState = PlayerStates.IDLE
                self.enableCollision = True
                
        elif self.state == PlayerStates.JUMP:
            if newState in [PlayerStates.IDLE,PlayerStates.WALK,PlayerStates.CROUCH,PlayerStates.TURN]:
                newState = PlayerStates.JUMP

        elif self.state == PlayerStates.DASH:
            if self.springCollided:
                self.dashState = "end"
                newState = newState 
                self.dashFrameCounter = 0
            elif self.dashFrameCounter >= DASH_DURATION + DASH_SLOW_UP_DURATION + DASH_SLOW_DOWN_DURATION:
                self.dashState = "end"
                newState = PlayerStates.IDLE if newState == PlayerStates.JUMP else newState
                self.dashFrameCounter = 0
            else:
                newState = self.state
                
        elif self.state == PlayerStates.TURN:
            if newState == PlayerStates.JUMP:
                newState = PlayerStates.JUMP

            elif self.spriteID == "turn8":
                newState = PlayerStates.WALK

        elif self.state in [PlayerStates.WALK,PlayerStates.IDLE,PlayerStates.CROUCH]:
            pass

        return newState
    
    def move(self, vector: tuple[int, int, int]) -> None:
        """
        Move the player
        
        Args:
            vector (tuple[int, int]): movement vector

        Returns:
            None
        """
        #?vector:(x,y,dash, look up?)
        newState = self.newstate(vector)
        
        if self.state != newState:
            self.spriteID = f"{newState.value}1"
            self.animationFrameCounter = 0
        self.state = newState

        #dash state
        if self.state == PlayerStates.DASH:
            if self.dashState == "fast":
                newVector = (0,0,vector[2],vector[3])
                vector = newVector
            self.dash()
            #stop other movements during the first step of the dash

        elif self.state == PlayerStates.JUMP:
          self.jump()
            
        #turning left or right
        elif self.state in [PlayerStates.TURN]:
            self.turn()
        
        elif self.state in [PlayerStates.WALK]:
            self.walk()
            
        elif self.state in [PlayerStates.CROUCH]:
            self.crouch()
            
        elif self.state in [PlayerStates.IDLE]:
            self.idle()
        elif self.state in [PlayerStates.RESPAWN]:
            self.respawn()
            
        #update particles and remove the ones that are done
        for particle in self.particles:
            if particle.update():
                self.particles.remove(particle)
        if self.enableCollision:
            #!The sprite rect still has the old position, so we need to update it first
            self.y += Y_GRAVITY
            self.sprite.rect.y = self.y
            #ceiling and ground

            touchedGround = False
            collided = False
            for tile in self.serviceLocator.map.walls:
                if self.sprite.rect.colliderect(tile.rect):
                    #ceiling
                    if tile.rect.bottom - self.sprite.rect.top <= DASH_SPEED:
                        # print("ceiling")
                        self.y = tile.rect.bottom
                    #ground
                    elif tile.rect.top - self.sprite.rect.bottom >= -1*DASH_SPEED:
                        #add land particle (same as jump)
                        if self.wasGrounded == False:
                            touchedGround = True

                        # print("ground")
                        collided = True
                        self.wasGrounded = True
                        self.coyoteCounter = COYOTE_COUNTER
                        self.y = tile.rect.top - self.height
                        #reset dash
                        if self.state != PlayerStates.DASH:
                            self.dashCount = 1
                            self.dashRefreshTimer = 0
                            self.dashState = "end"

                        if self.jumpState == PlayerJumpStates.DOWN:
                            if newState == PlayerStates.JUMP: # prevents a bug
                                newState = PlayerStates.IDLE#
                            self.jumpState = PlayerJumpStates.INIT#
                            self.state = newState
                            self.spriteID = f"{newState.value}1"
                            self.animationFrameCounter = 0
                            
                        for obs in self.observers:
                            obs.notify(self.name,"ground")

                        #prevent non collisions to further change wasgrounded
                        break
        
            if not collided:
                self.wasGrounded = False
            
            if touchedGround:
                self.particles.append(SpriteParticle(self.x + self.width/2,self.y + self.height/2,"jump"))


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
                    self.serviceLocator.display.fill((255,0,0),tile.rect)

                    # print("subtraction ",tile.rect.left - self.sprite.rect.right)
                    # print("speed ",-1*DASH_SPEED)
                    
                    #left wall
                    if tile.rect.right - self.sprite.rect.left <=  DASH_SPEED:
                        # print("left wall")
                        self.x = tile.rect.right
                    #right wall
                    elif tile.rect.left - self.sprite.rect.right >= -1*DASH_SPEED:
                        # print("right wall")
                        self.x = tile.rect.left - self.width
                        # print("x rectify",self.x)
              
              

                
            #check collisions for the rest of the actors
            for actor in self.serviceLocator.actorList:
                if actor.type == ActorTypes.DASH_RESET:
                    #if the dash reset is on and the player ha sno dashes, after collision, reset the dash and notify the dash reset entity
                    if self.dashCount == 0 and actor.state =="idle" and self.sprite.rect.colliderect(actor.sprite.rect):
                        self.dashCount = 1
                        #notify observers
                        for obs in self.observers:
                            obs.notify(actor.name,"dashReset")
                            
                if actor.type == ActorTypes.SPRING:
                    if self.sprite.rect.colliderect(actor.sprite.rect) and self.springCollsionCooldown == 0:
                        for obs in self.observers:
                            obs.notify(actor.name,"springCollision")
                            self.springCollided = True
                            self.springCollsionCooldown = SPRING_COLLISION_COOLDOWN
                        #self.playSound("spring",1)
                        self.serviceLocator.soundManager.play("spring")

                if actor.type == ActorTypes.STRAWBERRY:
                    if self.sprite.rect.colliderect(actor.sprite.rect) and actor.state == "idle":
                        #notify observers
                        for obs in self.observers:
                            obs.notify(actor.name,"strawberryCollected")
                        #self.playSound("strawberry",1)
                        self.serviceLocator.soundManager.play("strawberry")
                            
                #!PORCO
                if actor.type == ActorTypes.SPIKE or self.y > HEIGHT:
                    if self.sprite.rect.colliderect(actor.sprite.rect):
                        #notify observers
                        for obs in self.observers:
                            obs.notify(actor.name,"spikeCollision")
                        self.alive = False
                        self.x = self.spawnX
                        self.y = 800
                        #self.playSound("death",1)
                        self.serviceLocator.soundManager.play("death")



        #update orientation
        if vector[0] > 0:
            self.orientation = PlayerOrientation.RIGHT 
        elif vector[0] < 0 and self.state != PlayerStates.DASH:
            self.orientation = PlayerOrientation.LEFT
        
        self.animationFrameCounter += 1
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID,self.orientation == PlayerOrientation.LEFT)
        pygame.draw.rect(self.serviceLocator.display,(0,0,255),self.sprite.rect,1)

    #draws the hair
    def drawHair(self, display):
        #offset for the orientation of the character
        # print(self.state,self.spriteID)
        offsetDirX = PlayerStuff.spritesHairOffset[self.state][self.spriteID][0] + 8 if self.orientation == PlayerOrientation.RIGHT else PlayerStuff.spritesHairOffset[self.state][self.spriteID][0]*-1 - 8
        offsetDirY = PlayerStuff.spritesHairOffset[self.state][self.spriteID][1] + 12
        for i in range (len(points)-1,-1,-1):
            if i == 0:
                points[i][2] = pygame.Vector2(int(self.x + self.width / 2 +offsetDirX), int(self.y + self.height / 2-offsetDirY))
                continue
            if self.orientation == PlayerOrientation.RIGHT:
                points[i][2] = points[i][0] + points[i-1][2] 
            else:
                points[i][2] =  points[i-1][2]+(points[i][0][0]*-1,points[i][0][1])

        for i in range(len(points)):
            if i == 0:
                continue
            if self.orientation == PlayerOrientation.RIGHT:
                if points[i][2].distance_to(points[i][0]+points[i-1][2]) > points[i][1]:
                    dir = (points[i][2]-(points[i-1][2]+points[i][0])).normalize()
                    offset = dir * points[i][1]
                    points[i][2] = points[i-1][2] + points[i][0]+ offset
            else:
                if points[i][2].distance_to((points[i][0][0]*-1,points[i][0][1])+points[i-1][2]) > points[i][1]:
                    dir = (points[i][2]-(points[i-1][2]+(points[i][0][0]*-1,points[i][0][1]))).normalize()
                    offset = dir * points[i][1]
                    points[i][2] = points[i-1][2] + (points[i][0][0]*-1,points[i][0][1])+ offset
            
                
        
        for i in range (len(points)-1,-1,-1):
            if self.wasGrounded:
                if self.dashRefreshTimer <= 0:
                    pygame.draw.circle(display, (172, 50, 49), points[i][2], points[i][3]) # brown
                else:
                    pygame.draw.circle(display, (255, 255, 255), points[i][2], points[i][3]) # white
            else:
                if self.dashCount <= 0:
                    pygame.draw.circle(display, (69, 194, 255), points[i][2], points[i][3]) # blue
                else:
                    pygame.draw.circle(display, (172, 50, 49), points[i][2], points[i][3]) # brown
            # pygame.draw.circle(display, (0, 0, 0), points[i][2], points[i][3],width = 3) # brown
                    


    
    def draw(self,display: pygame.display) -> None:
        """
        Draw the player	and its hair

        Args:   
            display (pygame.display): display to draw the player
        
        Returns:
            None
        """
        #draw hair first to be behind the player
        self.drawHair(display)
        self.sprite.draw(display)
        for particle in self.particles:
            particle.draw(display)



    def update(self) -> None:
        pass
    def notify(self,actor,event):
        pass
    
    def levelComplete(self):
        if self.y < 0:
            return True
        else:
            return False
