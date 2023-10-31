from enum import Enum

class ActorTypes(Enum):
    PLAYER = 1
    ENEMY = 2
    NPC = 3
    DASH_RESET = 4
    STRAWBERRY = 5
    SPRING = 6

class PlayerStates(Enum):
    IDLE = "idle"
    WALK = "walk"
    JUMP = "jump"
    CROUCH = "crouch"
    DASH = "dash"
    TURN = "turn"

class PlayerJumpStates(Enum):
    INIT = 1
    UP = 2
    SLOWUP = 3
    SLOWDOWN = 4
    DOWN = 5

class PlayerOrientation(Enum):
    LEFT = 1
    RIGHT = 2
