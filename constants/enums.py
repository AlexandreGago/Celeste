from enum import Enum

class ActorTypes(Enum):
    PLAYER = 1
    ENEMY = 2
    NPC = 3
    DASH_RESET = 4
    STRAWBERRY = 5
    SPRING = 6
    SPIKE = 7
    FALLINGBLOCK = 8
    CLOUD = 9
    DASH_UPGRADE = 10
    DOUBLE_DASH_RESET = 11
    
class ParticleTypes(Enum):
    JUMP = 1
    
class PlayerStates(Enum):
    IDLE = "idle"
    WALK = "walk"
    JUMP = "jump"
    CROUCH = "crouch"
    DASH = "dash"
    TURN = "turn"
    RESPAWN = "respawn"
    WALLHUG = "wallhug"
    LOOKUP = "lookup"
    FALLING = "falling"

class PlayerJumpStates(Enum):
    INIT = 1
    UP = 2
    SLOWUP = 3
    SLOWDOWN = 4
    DOWN = 5

class PlayerOrientation(Enum):
    LEFT = 1
    RIGHT = 2

class SpikeOrientations(Enum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4

class EventType(Enum):
    DASH_RESET_COLLISION = 1
    SPRING_COLLISION = 2
    STRAWBERRY_COLLISION = 3
    FALLINGBLOCK_COLLISION = 4
    SPIKE_COLLISION = 5
    DASH_UPGRADE_COLLISION = 6
    GROUND_COLLISION = 7
    DOUBLE_DASH_RESET_COLLISION = 8