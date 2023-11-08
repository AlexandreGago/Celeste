import pygame
# import utils.utils as utils
import utils
from constants.dictionaries import physicsValues
import time
from constants.enums import ActorTypes,PlayerStates,PlayerOrientation

ground = physicsValues.ground
air = physicsValues.air
jump = physicsValues.jump
dash = physicsValues.dash

def calculateSpeed(val:int, target:int, amount:int) -> int:
    """
    Accelerate or decelerate but don't overshoot the target

    Args:
        val (int): current value
        target (int): target value
        amount (int): amount to change by

    Returns:
        int: new value
    """
    #if the value is greater than the target, decelerate
    if val > target:
        #decelerate val by amount but don't go below the target
        result = max(val-amount, target)
    else:
        #accelerate val by amount but don't go above the target
        result = min(val+amount, target)
    return result

    

class Physics():
    def __init__(self):
        self.speed = [0,0]
    
    def move(self,x,y,xInput,yInput,dashInput,jumpInput,collisions,orientation) -> tuple[float,float]:
        """
        Calculate new position based on inputs and collisions

        Args:
            x (int): current x position
            y (int): current y position

            xInput (int): -1 for left, 1 for right, 0 for no input
            yInput (int): 1 for up, -1 for down, 0 for no input
            dashInput (bool) : True if dash button is pressed
            jumpInput (bool) : True if jump button is pressed
            collisions (list): list of collisions [left,right,top,bottom] -> True if colliding
            orientation (int): orientation -> PlayerOrientation.RIGHT/LEFT

        Returns:
            tuple[float,float]: new position
        """
        surface = ground if collisions[3] else air #! collisions still not 100% working (flickering) so the surface isnt correct
        #TODO : add air acceleration 
        #if over the speed limit, decelerate
        if abs(self.speed[0]) > ground["maxSpeed"]:
            #get the sign of the speed to determine which way to decelerate
            sign = 1 if self.speed[0] > 0 else -1 if self.speed[0] < 0 else 0
            self.speed[0] = calculateSpeed(self.speed[0], surface["maxSpeed"] * sign , surface["deceleration"])
        #if under the speed limit, accelerate, but don't overshoot the limit
        #movement[0] is the direction the player is trying to move
        else:
            self.speed[0] = calculateSpeed(self.speed[0], xInput * surface["maxSpeed"], surface["acceleration"])
    
        #!COYOTE
        #if player pressed jump and is grounded, jump
        if jumpInput and collisions[3]:
            self.speed[1] = -jump["power"]
        
        else:

            #if we are in the air, apply gravity
            if self.speed[1] > air["maxSpeed"]:
                self.speed[1] = calculateSpeed(self.speed[1], air["maxSpeed"], - air["gravity"])
            else:
                self.speed[1] = calculateSpeed(self.speed[1], air["maxSpeed"], air["gravity"])

            

        if dashInput: #Dash
            if xInput == 0 and yInput == 0:
                xInput = 1 if orientation == PlayerOrientation.RIGHT else -1
            self.speed[0] = dash["power"] * xInput
            self.speed[1] = dash["power"] * -yInput

        # if yInput == -1 and not collisions[3]: # if we are crouching we cant move #! collsions still not working, so this isnt either
        #     pass
        # else:
        x += self.speed[0]
        y += self.speed[1]
        return x,y

    def update(self):
        x += self.speed[0]
        y += self.speed[1]

    def reset(self):
        self.speed = [0,0]
        self.grounded = False
        self.orientation = PlayerOrientation.RIGHT
        
    def rollbacl(self, speed):
        self.speed = speed
        
