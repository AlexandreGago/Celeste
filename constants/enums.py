from enum import Enum

class ActorTypes(Enum):
    PLAYER = 1
    ENEMY = 2
    NPC = 3
    DASH_RESET = 4
    STRAWBERRY = 5

class PlayerStates(Enum):
    IDLE = 1
    WALK = 2
    JUMP = 3
    CROUCH = 4
    DASH = 5
    TURNING = 6