from actors.actor import Actor
import pygame
import pygame.gfxdraw
from constants.enums import ActorTypes,PlayerStates,PlayerOrientation,EventType,States
from constants.dictionaries import PlayerDicts, physicsValues
from spriteClass import SpriteClass

from actors.spriteParticle import SpriteParticle
from utils.physics import Physics
import utils.utils as utils


# MAX_DASHES = 2
DASH_COOLDOWN = 1
PLAYERWIDTH = 49
PLAYERHEIGHT = 49
WALLGRACE = 5
COYOTEJUMP = 10
WALLJUMP_COOLDOWN = 10

ANIMATION_SPEEDS = {
    "jump": 10,
    "turn": 2,
    "dash" : 1
}


class Player(Actor):
    def __init__(self,x:int,y:int,name:str,serviceLocator) -> None:
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
        #player localizations
        self.spawnX = x
        self.spawnY = y
        self.x = x
        self.y = serviceLocator.map.height
        
        #play type
        self.type = ActorTypes.PLAYER
        
        #physics
        self.physics = Physics()
        
        #call the parent constructor (Actor)
        super().__init__(x,serviceLocator.map.height,50,50,serviceLocator)
        self.name = name
        self.serviceLocator = serviceLocator

        #collisions
        self.collisions = [0,0,0,0]
        
        #player size and state
        self.height = PLAYERHEIGHT
        self.width = PLAYERWIDTH
        self.orientation = PlayerOrientation.RIGHT
        self.state = PlayerStates.RESPAWN
        self.alive = False
        
        #sprite
        self.spriteID = f"{self.state.value}1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID,playerName=self.name)
        self.animationFrameCounter = 0
        
        #dash
        self.currentDashCount = 2 #!this will increase when we get the dash upgrade
        self.dashCount = self.currentDashCount 
        #Particles
        self.particles = []
        
        self.springCollided = False

        self.airborne = 0

        #Grace periods
        self.wallGrace = 0
        self.coyoteJump = 0

        #Cooldowns
        self.dashCooldown = 0
        self.wallJumpCooldown = 0

        self.wallJumpSide = 0 # -1 for right, 1 for left

        self.hairPoints = [#offset, max_distance, position, size
            [pygame.Vector2(0,0),0,pygame.Vector2(0,0),15], #first point is the center of the head
            [pygame.Vector2(-6,4),9,pygame.Vector2(0,0),14],
            [pygame.Vector2(-2,4),8.5,pygame.Vector2(0,0),13],
            [pygame.Vector2(-4,4),8,pygame.Vector2(0,0),12], 
            [pygame.Vector2(-4,2),7.5,pygame.Vector2(0,0),11],
            [pygame.Vector2(-2,2),7,pygame.Vector2(0,0),10],
        ]
        
        return
    
    def spawn(self) -> None:
        """
        Spawns the player

        Args:
            None

        Returns:
            None
        """
        if self.y > self.spawnY:    
            self.y -= 8
        else:
            return True
        return False
    
    def levelComplete(self) -> bool:
        """
        Checks if the player is above the screen

        Args:
            None

        Returns:
            bool: True if the player is above the screen, False otherwise
        """
        if self.y < 0:
            return True
        else:
            return False  
        
    def respawn(self) -> None:
        """
        Respawn State
        -Checks if the player is alive and if he is, changes the state to IDLE

        Args:
            None

        Returns:    
            None
        """
        self.alive = self.spawn() # check if the player is alive
        if self.alive: # if the player is alive, change the state to idle, reset the physics and reset the sprite
            self.state = PlayerStates.IDLE
            self.spriteID = f"{self.state.value}1"
            self.animationFrameCounter = 0
            self.physics.reset()

    def jump(self) -> None:
        """
        Jump State
        -Updates the sprite

        Args:
            None

        Returns:
            None
        """
        if self.animationFrameCounter % 10 == 0: # update the spite every 10 frames
            self.spriteID = PlayerDicts.sprites[self.spriteID]
        pass
    
    def dash(self) -> None:
        """
        Dash State
        -Updates the sprite

        Args:
            None

        Returns:
            None
        """
        if self.animationFrameCounter % 10 == 0:# update the spite every 10 frames
            self.spriteID = PlayerDicts.sprites[self.spriteID]

    def turn(self) -> None:
        """
        Turn State
        -Updates the sprite

        Args:
            None

        Returns:
            None
        """
        if self.animationFrameCounter % ANIMATION_SPEEDS["turn"] == 0:# update the spite every 2 frames
            self.spriteID = PlayerDicts.sprites[self.spriteID]
            
    def idle(self) -> None:
        """
        Idle State
        -Updates the sprite

        Args:
            None

        Returns:
            None
        """
        if self.animationFrameCounter % 10 == 0:# update the spite every 10 frames
            self.spriteID = PlayerDicts.sprites[self.spriteID]

    def walk(self) -> None:
        """
        Walk State
        -Updates the sprite

        Args:
            None

        Returns:
            None
        """
        if self.animationFrameCounter % 10 == 0:# update the spite every 10 frames
            self.spriteID = PlayerDicts.sprites[self.spriteID]

    def crouch(self) -> None:
        """
        Crouch State
        -Updates the sprite

        Args:
            None

        Returns:
            None
        """
        if self.animationFrameCounter % 10 == 0:# update the spite every 10 frames
            self.spriteID = PlayerDicts.sprites[self.spriteID]
            
    def lookup(self) -> None:
        """
        LookUp State
        -Updates the sprite

        Args:
            None

        Returns:
            None
        """
        if self.animationFrameCounter % 10 == 0:# update the spite every 10 frames
            self.spriteID = PlayerDicts.sprites[self.spriteID]

    def falling(self) -> None:
        """
        Falling State
        -Updates the sprite

        Args:
            None

        Returns:
            None
        """
        if self.animationFrameCounter % 10 == 0:# update the spite every 10 frames
            self.spriteID = PlayerDicts.sprites[self.spriteID]
    
    def updateState(self,xInput:int,yInput:int,dashInput:int,jumpInput:int) -> PlayerStates:
        """"
        This function decides the state of the player based on the inputs and the current state
        it is done after the move function so that the collisions are updated

        Args:
            xInput (int): x input
            yInput (int): y input
            dashInput (int): dash input
            jumpInput (int): jump input

        Returns:
            PlayerStates: the new state
        """
        newState = self.vectorToState(xInput,yInput,dashInput,jumpInput)
        
        #reduce the dash cooldown
        if self.state != PlayerStates.DASH : # dash cooldown
            self.dashCooldown -= 1 if self.dashCooldown > 0 else 0
                        #spring collision

        #reset dash count if we collide with a spring and set the newState to jump (the physics handles the speed of the jump)
        if self.springCollided:
            self.dashCount = self.currentDashCount
            newState = PlayerStates.JUMP
            
        #if we are dead, respawn
        if not self.alive :
            newState = PlayerStates.RESPAWN
        #we are alive
        #!this was in every state, so to reduce repetion, it is here
        elif xInput < 0 and self.collisions[0] and not self.collisions[3] and newState != PlayerStates.DASH: # change to wallhug
            newState = PlayerStates.WALLHUG
            self.wallGrace = WALLGRACE
            self.wallJumpSide = -1 if self.orientation == PlayerOrientation.LEFT else 1 if self.orientation == PlayerOrientation.RIGHT else self.wallJumpSide
        elif xInput > 0 and self.collisions[1] and not self.collisions[3]and newState != PlayerStates.DASH: # change to wallhug
            newState =  PlayerStates.WALLHUG
            self.wallGrace = WALLGRACE
            self.wallJumpSide = -1 if self.orientation == PlayerOrientation.LEFT else 1 if self.orientation == PlayerOrientation.RIGHT else self.wallJumpSide
        #!---
        else:
            #if we are jumping, keep jumping unless we are dashing
            if self.state == PlayerStates.JUMP:
                if newState != PlayerStates.DASH and self.airborne == -1:
                    newState = PlayerStates.JUMP
                elif self.airborne == 1:
                    newState = PlayerStates.FALLING
                    
            elif self.state == PlayerStates.DASH:
                if self.orientation == PlayerOrientation.RIGHT:
                    if self.physics.speed[0] > physicsValues.air["maxSpeed"] or self.physics.speed[1] < -physicsValues.air["maxSpeed"]:
                        newState = PlayerStates.DASH
                else:
                    if self.physics.speed[0] < -physicsValues.air["maxSpeed"] or self.physics.speed[1] < -physicsValues.air["maxSpeed"]: # of the speed is greater than the max speed, keep dashing
                        newState = PlayerStates.DASH
                if self.airborne != 0:
                    newState = PlayerStates.FALLING

            elif self.state in [PlayerStates.TURN]:
                if newState in [PlayerStates.JUMP,PlayerStates.DASH]:  #!this can be removed for a smoother animation
                    pass
                elif self.spriteID != "turn8":
                    newState = PlayerStates.TURN
                
            elif self.state in [PlayerStates.WALK]:
                # if the nes state is jump or dash, exit walk and enter them
                if newState == PlayerStates.JUMP or newState == PlayerStates.DASH:  
                    pass
                elif ((self.orientation == PlayerOrientation.RIGHT) and (xInput == -1)) or (self.orientation == PlayerOrientation.LEFT and xInput > 0):
                    newState = PlayerStates.TURN
                elif self.airborne == 1:
                    newState = PlayerStates.FALLING

            elif self.state in [PlayerStates.WALLHUG]:
                self.wallGrace = WALLGRACE
                self.wallJumpSide = -1 if self.orientation == PlayerOrientation.LEFT else 1 if self.orientation == PlayerOrientation.RIGHT else self.wallJumpSide

                
            elif self.state in [PlayerStates.CROUCH]:
                pass 
                
            elif self.state in [PlayerStates.IDLE]:

                if newState == PlayerStates.JUMP or newState == PlayerStates.DASH:  
                    pass
                elif ((self.orientation == PlayerOrientation.RIGHT) and (xInput == -1)) or (self.orientation == PlayerOrientation.LEFT and xInput > 0):
                    newState = PlayerStates.TURN
                if self.airborne == 1:
                    newState = PlayerStates.FALLING

                
            elif self.state in [PlayerStates.RESPAWN]:
                if self.alive: #if the player is alive, change the state else maintain the state
                    pass
                else:
                    newState = PlayerStates.RESPAWN
                
            elif self.state in [PlayerStates.LOOKUP]:
                pass

            elif self.state in [PlayerStates.FALLING]:
                if newState == PlayerStates.DASH :  
                    pass
                elif self.airborne != 0:
                    newState = PlayerStates.FALLING

            elif self.state in [PlayerStates.LOOKUP]:
                pass
        
        return newState
    
    def move(self,vector:tuple) -> None:
        """
        Move the player and update the state and sprite
        -Parse the inputs
        -Move the player through the physics class
        -Check for collisions with terrain
        -Check if the player is in the air or on the ground
        -Check for collisions with the rest of the actors
        -Update the state based on the inputs and the current state
        -Update the orientation
        -Update the particles
        -Update the animation frame counter
        -Update the sprite

        Args:
            vector (tuple): (xInput,yInput,dashInput,jumpInput)

        Returns:
            None
        """
        #process inputs
        xInput,yInput,dashInput,jumpInput = vector # unpack the vector
        dashInput,wallJump,jumpInput = self.validateInput(dashInput,jumpInput)# validate the inputs ex: if jumpInput = 1 but we are in the air, jumpInput = 0
        if self.alive:# only move and change states if the player is alive
            #update the position of the player through the physics class
            temp_x,temp_y = self.physics.move(self.x,self.y,xInput,yInput,dashInput,jumpInput,self.collisions,self.orientation,self.springCollided,wallJump,self.state,self.wallJumpSide)
                
            #check for collisions with terrain, update the position if there is a collision
            self.checkCorrectCollisions(temp_x,temp_y) 
            #check if the player is in the air (descending or ascending) or on the ground
            self.updateAirborne()
            #check for collisions with the rest of the actors
            self.actorCollision()

            #update the state after the move
            newState = self.updateState(xInput,yInput,dashInput,jumpInput)
            # check if the state changed and do the corresponding actions
            self.checkStateChange(newState) 
            # change state
            self.state = newState 
        
        #update orientation (cannot be moved up because it is used by updateState)
        self.orientation = self.updateOrientation(xInput)
        
        #update the sprite corresponding to the state
        self.updateSprite()
        
        #update particles and remove the ones that are done
        if self.physics.speed[0] > 10 or self.physics.speed[0] <-10 or self.physics.speed[1] >10 or self.physics.speed[1] < -10:
            self.particles.append(SpriteParticle(self.x + self.width/2,self.y + (self.height/2),"jump"))

        for particle in self.particles:
            if particle.update():
                self.particles.remove(particle)
        
        #advance the animationFrameCounter
        self.animationFrameCounter += 1 if self.animationFrameCounter <= 60 else -59 
        #update the sprite #! can be called in updateSprite() for optimization
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID,self.orientation == PlayerOrientation.LEFT,playerName=self.name)
        
    #draws the hair
    def drawHair(self, display:pygame.display) -> None:
        """
        Draw the hair of the player
        -The hair are a bunch of circles that follow each other

        Args:
            display (pygame.display): display to draw the hair

        Returns:
            None
        """
        #offset for the orientation of the character
        if PlayerDicts.spritesHairOffset[self.state][self.spriteID]:
            offsetDirX = PlayerDicts.spritesHairOffset[self.state][self.spriteID][0] + 8 if self.orientation == PlayerOrientation.RIGHT else PlayerDicts.spritesHairOffset[self.state][self.spriteID][0]*-1 - 8
            offsetDirY = PlayerDicts.spritesHairOffset[self.state][self.spriteID][1] + 12
        for i in range (len(self.hairPoints)-1,-1,-1):
            if i == 0:
                self.hairPoints[i][2] = pygame.Vector2(int(self.x + self.width / 2 +offsetDirX), int(self.y + self.height / 2-offsetDirY))
                continue
            if self.orientation == PlayerOrientation.RIGHT:
                self.hairPoints[i][2] = self.hairPoints[i][0] + self.hairPoints[i-1][2] 
            else:
                self.hairPoints[i][2] =  self.hairPoints[i-1][2]+(self.hairPoints[i][0][0]*-1,self.hairPoints[i][0][1])

        for i in range(len(self.hairPoints)):
            if i == 0:
                continue
            if self.orientation == PlayerOrientation.RIGHT:
                if self.hairPoints[i][2].distance_to(self.hairPoints[i][0]+self.hairPoints[i-1][2]) > self.hairPoints[i][1]:
                    dir = (self.hairPoints[i][2]-(self.hairPoints[i-1][2]+self.hairPoints[i][0])).normalize()
                    offset = dir * self.hairPoints[i][1]
                    self.hairPoints[i][2] = self.hairPoints[i-1][2] + self.hairPoints[i][0]+ offset
            else:
                if self.hairPoints[i][2].distance_to((self.hairPoints[i][0][0]*-1,self.hairPoints[i][0][1])+self.hairPoints[i-1][2]) > self.hairPoints[i][1]:
                    dir = (self.hairPoints[i][2]-(self.hairPoints[i-1][2]+(self.hairPoints[i][0][0]*-1,self.hairPoints[i][0][1]))).normalize()
                    offset = dir * self.hairPoints[i][1]
                    self.hairPoints[i][2] = self.hairPoints[i-1][2] + (self.hairPoints[i][0][0]*-1,self.hairPoints[i][0][1])+ offset
            
                
        for i in range (len(self.hairPoints)-1,-1,-1):
            pygame.draw.circle(display, (0, 0, 0), self.hairPoints[i][2], self.hairPoints[i][3]*self.width/50+3,3) # black border around hair
            
        for i in range (len(self.hairPoints)-1,-1,-1):
            if self.airborne == 0:
                if self.dashCooldown > 0:
                    pygame.draw.circle(display, (255, 255, 255), self.hairPoints[i][2], self.hairPoints[i][3]*self.width/50) # white
                else:
                    if self.dashCount <= 1:
                        pygame.draw.circle(display, (172, 50, 49), self.hairPoints[i][2], self.hairPoints[i][3]*self.width/50) # brown
                    else:
                        pygame.draw.circle(display, (50, 172, 49), self.hairPoints[i][2], self.hairPoints[i][3]*self.width/50) # green
            else:
                if self.dashCount <= 0:
                    pygame.draw.circle(display, (69, 194, 255), self.hairPoints[i][2], self.hairPoints[i][3]*self.width/50) # blue
                else:
                    if self.dashCount <= 1:
                        pygame.draw.circle(display, (172, 50, 49), self.hairPoints[i][2], self.hairPoints[i][3]*self.width/50) # brown
                    else:
                        pygame.draw.circle(display, (50, 172, 49), self.hairPoints[i][2], self.hairPoints[i][3]*self.width/50) # green
            # pygame.draw.circle(display, (172, 50, 49), points[i][2], points[i][3],width = 3) # brown
                    


    
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
    
    
    def validateInput(self,dashInput:int,jumpInput:int) -> tuple:
        """
        Validates the inputs
        -Checks if the dash is allowed
        -Checks if the jump is allowed
        -Checks if the we are walljumping
        -Reduces the wallgrace
        -Reduces the coyoteJump
        -Reduces the wallJumpCooldown

        Args:
            dashInput (int): dash input
            jumpInput (int): jump input

        Returns:
            tuple: dashInput,wallJump,jumpInput
        """
        dashInput, jumpInput = bool(dashInput), bool(jumpInput)
        dashInput = dashInput and self.dashCount >=1 and self.dashCooldown <= 0 #if we have dashes and the cooldown is over, dash allowed
        #decide if we are walljumping
        wallJump = jumpInput and (self.state == PlayerStates.WALLHUG or self.wallGrace > 0) and self.wallJumpCooldown <= 0

        if wallJump:
            self.wallJumpCooldown = WALLJUMP_COOLDOWN
        #decide if the jump is valid
        jumpInput = jumpInput and self.airborne >= 0 and (self.collisions[3] or self.coyoteJump > 0) and self.state != PlayerStates.JUMP
        #reduce the wallgrace
        self.wallGrace -= 1 if self.wallGrace > 0 else 0    
        self.coyoteJump -= 1 if self.coyoteJump > 0 else 0
        self.wallJumpCooldown -= 1 if self.wallJumpCooldown > 0 else 0

        return dashInput,wallJump,jumpInput
    
    def checkCollisionY(self,rect:pygame.Rect,x:int,y:int,up:bool,down:bool) -> tuple:
        upCollision,downCollision = False,False
        if self.sprite.rect.colliderect(rect):
            #ceiling
            if rect.rect.bottom - self.sprite.rect.top <= physicsValues.dash["power"] *1.3 and down:
                self.collisions[2] = 1
                # self.physics.speed[1] = 0
                self.sprite.rect.y = rect.rect.bottom
                # self.serviceLocator.display.fill((255,0,0),rect.rect)

                downCollision = True

            #floor
            elif rect.rect.top - self.sprite.rect.bottom >= - physicsValues.dash["power"]*1.3 and up:
                self.collisions[3] = 1
                self.physics.speed[1] = 0
                self.dashCount = self.currentDashCount
                self.coyoteJump = COYOTEJUMP

                # self.serviceLocator.display.fill((255,0,0),rect.rect)

                upCollision = True

        return upCollision,downCollision


    def checkCollisionX(self,rect:pygame.Rect,x:int,y:int,left:bool,right:bool) -> tuple:
        leftCollision,rightCollision = False,False
        if self.sprite.rect.colliderect(rect):
            #left
            if rect.rect.right - self.sprite.rect.left <= physicsValues.dash["power"]*1.3 and left:
                self.collisions[0] = 1
                # self.physics.speed[0] = 0
                self.sprite.rect.x = rect.rect.right

                leftCollision = True

                # self.serviceLocator.display.fill((255,0,0),rect.rect)
            #right
            elif rect.rect.left - self.sprite.rect.right >= - physicsValues.dash["power"]*1.3 and right:
                self.collisions[1] = 1
                self.physics.speed[0] = 0
                x = rect.rect.left - self.width
                self.sprite.rect.x = x
                # self.serviceLocator.display.fill((255,0,0),rect.rect)

                rightCollision = True

        return leftCollision,rightCollision

    def checkCorrectCollisions(self,x:int,y:int) -> None:
        """
        Checks for collisions with the terrain and updates the position if there is a collision

        Args:
            x (int): x position
            y (int): y position

        Returns:
            None
        """
        self.collisions = [0,0,0,0]

        self.sprite.rect.y = y
        for tile in self.serviceLocator.map.walls:
            up,down = self.checkCollisionY(tile,x,y,True,True)
            if up:
                self.sprite.rect.y = tile.rect.top - self.height


        self.sprite.rect.x = x
        for tile in self.serviceLocator.map.walls:
            self.checkCollisionX(tile,x,y,True,True)

        fallingBlockCollision = False # this serves to check every falling block, without this, only the firt one is detetcted
        fallingBlockSpriteCollided = None
        
        for actor in self.serviceLocator.actorList:
            if actor.type == ActorTypes.CLOUD:
                sprite = actor.sprite
                if self.airborne >= 0:
                    up,down = self.checkCollisionY(sprite,x,y,True,False)
                    if up:
                        self.sprite.rect.y = sprite.rect.top - self.height

            if actor.type == ActorTypes.FALLINGBLOCK:
                sprite = actor.sprite
                if self.airborne >= 0 and actor.state != States.OUTLINE:
                    up,down = self.checkCollisionY(sprite,x,y,True,False)
                    if up:
                        for obs in self.observers:
                            obs.notify(actor.name,EventType.FALLINGBLOCK_COLLISION)
                        fallingBlockCollision = True
                        fallingBlockSpriteCollided = sprite

        if fallingBlockCollision:#falling block collision
            self.sprite.rect.y = fallingBlockSpriteCollided.rect.top - self.height

        #check if we are out of bounds
        if self.sprite.rect.x < 0:
            self.sprite.rect.x = 0
        if self.sprite.rect.x > self.serviceLocator.map.width - self.width:
            self.sprite.rect.x = self.serviceLocator.map.width  - self.width

        #notify observers of groud collision
        if self.collisions[3]:
            for obs in self.observers:
                obs.notify(self.name,EventType.GROUND_COLLISION)

        self.x = self.sprite.rect.x
        self.y = self.sprite.rect.y

    def updateOrientation(self,xInput:int) -> PlayerOrientation:
        """
        Updates the orientation of the player based on the xInput
        -If the xInput is positive, the orientation is right
        -If the xInput is negative, the orientation is left
        -If the xInput is 0, the orientation is the same as before
        Args:
            xInput (int): x input

        Returns:
            PlayerOrientation: the new orientation
        """
        return PlayerOrientation.RIGHT if xInput > 0 else PlayerOrientation.LEFT if xInput < 0 else self.orientation
    
    def updateAirborne(self) -> None:
        """
        Checks if the player is in the air (descending or ascending) or on the ground
        -If the speed is negative, the player is ascending
        -If the speed is positive, the player is descending
        -If the speed is 0, the player is on the ground

        Args:
            None

        Returns:
            None
        """
        #!check if we are in the air after the movement
        if self.physics.speed[1] < 0:
            self.airborne = -1
        elif self.physics.speed[1] > 0:
            self.airborne = 1
        else:
            if self.collisions[3]:
                self.airborne = 0
            else:
                self.airborne = -1

    def vectorToState(self,xInput:int,yInput:int,dashInput:int,jumpInput:int) -> PlayerStates:
        """
        Parses the inputs into a state

        Args:
            xInput (int): x input
            yInput (int): y input
            dashInput (int): dash input
            jumpInput (int): jump input

        Returns:
            PlayerStates: The state corresponding to the inputs
        """
        if dashInput == 1:
            return PlayerStates.DASH
        if jumpInput == 1:
            return PlayerStates.JUMP
        if xInput != 0:
            return PlayerStates.WALK
        if yInput == -1:
            return PlayerStates.CROUCH
        if yInput == 1:
            return PlayerStates.LOOKUP
        
        return PlayerStates.IDLE
    
    def checkStateChange(self,newState:PlayerStates) -> None:
        """
        Checks if the state changed and do the corresponding actions for the new state

        Args:
            newState (PlayerStates): the new state

        Returns:
            None
        """
        # if the state changed, reset the animation frame counter and the spriteID
        if self.state != newState:
            self.animationFrameCounter = 1
            self.spriteID = f"{newState.value}1"
            if newState == PlayerStates.DASH:# if the newState is a dash, reduce the dash count and reset the cooldown
                self.particles.append(SpriteParticle(self.x + self.width/2,self.y + self.height/2,"jump"))
                self.dashCount -= 1 if self.dashCount > 0 else 0 
                self.dashCooldown = DASH_COOLDOWN
                self.serviceLocator.soundManager.play("dash")
                self.serviceLocator.offset = utils.screen_shake(5,15,4)


            if newState == PlayerStates.JUMP: # id the newState is a jump, play the jump Sound
                self.particles.append(SpriteParticle(self.x + self.width/2,self.y + (self.height/3*2),"jump"))
                self.serviceLocator.soundManager.play("jump") 
        
    def updateSprite(self) -> None:
        """
        Updates the sprite of the player based on the state

        Args:
            None

        Returns:
            None
        """
        match self.state:
            case PlayerStates.JUMP:
                self.jump()
            case PlayerStates.DASH:
                self.dash()
            case PlayerStates.TURN:
                self.turn()
            case PlayerStates.WALK:
                self.walk()
            case PlayerStates.CROUCH:
                self.crouch()
            case PlayerStates.IDLE:
                self.idle()
            case PlayerStates.LOOKUP: 
                self.lookup()
            case PlayerStates.RESPAWN:
                self.respawn()
            case PlayerStates.FALLING:
                self.falling()
            case PlayerStates.LOOKUP:
                self.lookup()
            case _:
                pass

    def actorCollision(self) -> None:
        """
        Checks for collisions with the rest of the actors (except clouds and fallingBlock that are done in checkCollisions)

        Args:
            None

        Returns:
            None
        """
        #check collisions for the rest of the actors
        self.springCollided = False
        for actor in self.serviceLocator.actorList:
            if actor.type == ActorTypes.DASH_RESET:        
                #if the dash reset is on and the player ha sno dashes, after collision, reset the dash and notify the dash reset entity
                if self.dashCount <= self.currentDashCount-1 and actor.state ==States.IDLE and self.sprite.rect.colliderect(actor.sprite.rect):
                    self.dashCount +=1
                    self.dashCooldown = DASH_COOLDOWN
                    #notify observers
                    for obs in self.observers:
                        obs.notify(actor.name,EventType.DASH_RESET_COLLISION)

            if actor.type == ActorTypes.DOUBLE_DASH_RESET:
                if self.dashCount <= self.currentDashCount-1 and actor.state ==States.IDLE and self.sprite.rect.colliderect(actor.sprite.rect):
                    self.dashCount = self.currentDashCount if self.currentDashCount >= 2 else 2
                    self.dashCooldown = DASH_COOLDOWN
                    #notify observers
                    for obs in self.observers:
                        obs.notify(actor.name,EventType.DOUBLE_DASH_RESET_COLLISION)
                        
            if actor.type == ActorTypes.SPRING:
                if self.sprite.rect.colliderect(actor.sprite.rect) :#and self.springCollsionCooldown == 0:
                    for obs in self.observers:
                        obs.notify(actor.name,EventType.SPRING_COLLISION)
                    self.springCollided = True
                    # self.springCollsionCooldown = SPRING_COLLISION_COOLDOWN

            if actor.type == ActorTypes.STRAWBERRY:
                if self.sprite.rect.colliderect(actor.sprite.rect) and actor.state == States.IDLE:
                    #notify observers
                    for obs in self.observers:
                        obs.notify(actor.name,EventType.STRAWBERRY_COLLISION)
                    #self.playSound("strawberry",1)
                        
            if actor.type == ActorTypes.SPIKE :
                if self.sprite.rect.colliderect(actor.hitbox):
                    self.alive = False
                    self.x = self.spawnX
                    self.y = self.serviceLocator.map.height
                    self.physics.reset()
                    #self.playSound("death",1)
                    self.serviceLocator.soundManager.play("death")
            if self.y > self.serviceLocator.map.height:
                self.alive = False
                self.x = self.spawnX
                self.y = self.serviceLocator.map.height

            if actor.type == ActorTypes.DASH_UPGRADE:
                if actor.state == States.IDLE and self.sprite.rect.colliderect(actor.sprite.rect):
                    for obs in self.observers:
                        obs.notify(actor.name,EventType.DASH_UPGRADE_COLLISION)
                    self.currentDashCount += 1
                    self.dashCount = self.currentDashCount

    def reset(self,x:int,y):
        """
        Resets the player when changing level

        Args:
            x (int): x position
            y (int): y position

        Returns:
            None
        """
        self.x = x
        self.y = self.serviceLocator.map.height
        self.sprite.rect.x = x
        self.sprite.rect.y = self.serviceLocator.map.height

        self.spawnX = x
        self.spawnY = y
        
        self.physics.reset()

        self.state = PlayerStates.RESPAWN
        self.alive = False

        self.dashCount = self.currentDashCount
        self.dashCooldown = 0
        self.wallJumpCooldown = 0
        self.wallGrace = 0
        self.coyoteJump = 0
        self.wallJumpSide = 0
        self.airborne = 0
        self.orientation = PlayerOrientation.RIGHT
        self.animationFrameCounter = 0
        self.spriteID = f"{self.state.value}1"
        self.collisions = [0,0,0,0]
        self.springCollided = False
        self.particles = []
        self.hairPoints = [#offset, max_distance, position, size
            [pygame.Vector2(0,0),0,pygame.Vector2(0,0),15], #first point is the center of the head
            [pygame.Vector2(-6,4),9,pygame.Vector2(0,0),14],
            [pygame.Vector2(-2,4),8.5,pygame.Vector2(0,0),13],
            [pygame.Vector2(-4,4),8,pygame.Vector2(0,0),12], 
            [pygame.Vector2(-4,2),7.5,pygame.Vector2(0,0),11],
            [pygame.Vector2(-2,2),7,pygame.Vector2(0,0),10],
        ]
        


