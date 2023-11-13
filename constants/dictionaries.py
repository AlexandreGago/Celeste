import pygame
from constants.enums import PlayerStates


sounds={
    "song1":"./sounds/level.mp3",
    "death":"./sounds/madeline_death.wav",
    "strawberry":"./sounds/strawberry_red_get_1000.wav",
    "spring":"./sounds/spring.wav",
    "dash":"./sounds/dash_red_left.wav",
    "jump":"./sounds/jump.wav",
    "dashEntityReset":"./sounds/diamond_return_01.wav",
    "dashEntityBreak":"./sounds/diamond_touch_01.wav"
}

class physicsValues:
    ground = {
    "maxSpeed": 5,
    "acceleration": 0.51,
    "deceleration": 1,
    }
    
    air = {
        "maxSpeed": 5,
        "acceleration": 0.51,#x
        "deceleration": 0.5,
        "gravity": 0.5,
    }

    dash = {
        "power": 12,
    }
    spring = {
        "power": 12
    }
    jump = {
        "power": 10,
    }

class PlayerStuff:
    sprites = {
        "idle1":"idle2","idle2":"idle3","idle3":"idle4","idle4":"idle5","idle5":"idle6","idle6":"idle7","idle7":"idle8","idle8":"idle1",
        "walk1":"walk2","walk2":"walk3","walk3":"walk4","walk4":"walk5","walk5":"walk6","walk6":"walk7","walk7":"walk8","walk8":"walk9","walk9":"walk10","walk10":"walk11","walk11":"walk12","walk12":"walk1",
        "walkLeft1":"walkLeft2","walkLeft2":"walkLeft3","walkLeft3":"walkLeft4","walkLeft4":"walkLeft5","walkLeft5":"walkLeft6","walkLeft6":"walkLeft7","walkLeft7":"walkLeft8","walkLeft8":"walkLeft9","walkLeft9":"walkLeft10","walkLeft10":"walkLeft11","walkLeft11":"walkLeft12","walkLeft12":"walkLeft1",
        "turn1":"turn2","turn2":"turn3","turn3":"turn4","turn4":"turn5","turn5":"turn6","turn6":"turn7","turn7":"turn8","turn8":"turn8",
        "turningRight1":"turningRight2","turningRight2":"turningRight3","turningRight3":"turningRight4","turningRight4":"turningRight5","turningRight5":"turningRight6","turningRight6":"turningRight7","turningRight7":"turningRight8","turningRight8":"end",
        "crouch1":"crouch2","crouch2":"crouch3","crouch3":"crouch4","crouch4":"crouch1",
        "jump1":"jump2","jump2":"jump1",
        "dash1":"dash2","dash2":"dash3","dash3":"dash4","dash4":"dash1",
        "respawn1":"respawn1",
        "wallhug1":"wallhug1",
        "falling1":"falling2","falling2":"falling1",
        "lookup1":"lookup2","lookup2":"lookup3","lookup3":"lookup4","lookup4":"lookup5","lookup5":"lookup6","lookup6":"lookup7","lookup7":"lookup8","lookup8":"lookup5",
    }

    spritesHairOffset = {PlayerStates.IDLE:{"idle1":(0,5),"idle2":(0,5),"idle3":(0,5),"idle4":(0,5),"idle5":(0,0),"idle6":(0,0),"idle7":(0,0),"idle8":(0,0)},
                        PlayerStates.WALK:{"walk1":(5,5),"walk2":(5,0),"walk3":(5,0),"walk4":(5,0),"walk5":(5,10),"walk6":(5,5),"walk7":(5,0),"walk8":(5,0),"walk9":(5,0),"walk10":(5,0),"walk11":(5,10),"walk12":(5,5)},
                        PlayerStates.TURN:{"turn1":(0,0),"turn2":(0,0),"turn3":(0,0),"turn4":(0,0),"turn5":(0,0),"turn6":(0,0),"turn7":(0,0),"turn8":(0,0)},
                        PlayerStates.CROUCH:{"crouch1":(-1,-10),"crouch2":(-1,-10),"crouch3":(-1,-10),"crouch4":(-1,-10)},
                        PlayerStates.JUMP:{"jump1":(5,10),"jump2":(5,10)},
                        PlayerStates.DASH:{"dash1":(10,0),"dash2":(10,0),"dash3":(10,0),"dash4":(10,0)},
                        PlayerStates.RESPAWN:{"respawn1":(0,5)},
                        PlayerStates.WALLHUG:{"wallhug1":(0,5)},
                        PlayerStates.FALLING:{"falling1":(5,5),"falling2":(0,5)},
                        PlayerStates.LOOKUP:{"lookup1":(0,5),"lookup2":(0,0),"lookup3":(0,5),"lookup4":(-4,5),"lookup5":(-5,0),"lookup6":(-5,0),"lookup7":(-5,5),"lookup8":(-5,5)}
                        }
    
    vectorToState = {
        (0,0): PlayerStates.IDLE,
        (0,1): PlayerStates.CROUCH,
        (1,1):  PlayerStates.CROUCH,
        (-1,1): PlayerStates.CROUCH,
        (0,-1): PlayerStates.JUMP,
        (1,-1): PlayerStates.JUMP,
        (-1,-1): PlayerStates.JUMP,
        (1,0): PlayerStates.WALK,
        (-1,0): PlayerStates.WALK
    }

    spritesLocation={
        #respawn sprite
        "respawn1":"./CelesteSprites/Atlases/Gameplay/characters/player/idle00.png",
        #wallhug sprite
        "wallhug1": "./CelesteSprites/Atlases/Gameplay/characters/player/climb00.png",

        #default idle animation
        "idle1": "./CelesteSprites/Atlases/Gameplay/characters/player/idle00.png",
        "idle2": "./CelesteSprites/Atlases/Gameplay/characters/player/idle01.png",
        "idle3": "./CelesteSprites/Atlases/Gameplay/characters/player/idle02.png",
        "idle4": "./CelesteSprites/Atlases/Gameplay/characters/player/idle03.png",
        "idle5": "./CelesteSprites/Atlases/Gameplay/characters/player/idle04.png",
        "idle6": "./CelesteSprites/Atlases/Gameplay/characters/player/idle05.png",
        "idle7": "./CelesteSprites/Atlases/Gameplay/characters/player/idle06.png",
        "idle8": "./CelesteSprites/Atlases/Gameplay/characters/player/idle07.png",

        #Walking right
        "walk1": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast00.png",
        "walk2": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast01.png",
        "walk3": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast02.png",
        "walk4": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast03.png",
        "walk5": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast04.png",
        "walk6": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast05.png",
        "walk7": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast06.png",
        "walk8": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast07.png",
        "walk9": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast08.png",
        "walk10": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast09.png",
        "walk11": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast10.png",
        "walk12": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast11.png",
        

        #turning left
        "turn1": "./CelesteSprites/Atlases/Gameplay/characters/player/flip00.png",
        "turn2": "./CelesteSprites/Atlases/Gameplay/characters/player/flip01.png",
        "turn3": "./CelesteSprites/Atlases/Gameplay/characters/player/flip02.png",
        "turn4": "./CelesteSprites/Atlases/Gameplay/characters/player/flip03.png",
        "turn5": "./CelesteSprites/Atlases/Gameplay/characters/player/flip04.png",
        "turn6": "./CelesteSprites/Atlases/Gameplay/characters/player/flip05.png",
        "turn7": "./CelesteSprites/Atlases/Gameplay/characters/player/flip06.png",
        "turn8": "./CelesteSprites/Atlases/Gameplay/characters/player/flip07.png",


        #crouch
        "crouch1": "./CelesteSprites/Atlases/Gameplay/characters/player/duck.png",
        "crouch2": "./CelesteSprites/Atlases/Gameplay/characters/player/duck.png",
        "crouch3": "./CelesteSprites/Atlases/Gameplay/characters/player/duck.png",
        "crouch4": "./CelesteSprites/Atlases/Gameplay/characters/player/duck.png",

        #jump
        "jump1": "./CelesteSprites/Atlases/Gameplay/characters/player/jumpFast00.png",
        "jump2": "./CelesteSprites/Atlases/Gameplay/characters/player/jumpFast01.png",

        #falling
        "falling1": "./CelesteSprites/Atlases/Gameplay/characters/player/jumpFast02.png",
        "falling2": "./CelesteSprites/Atlases/Gameplay/characters/player/jumpFast03.png",

        #dash
        "dash1": "./CelesteSprites/Atlases/Gameplay/characters/player/dash00.png",
        "dash2": "./CelesteSprites/Atlases/Gameplay/characters/player/dash01.png",
        "dash3": "./CelesteSprites/Atlases/Gameplay/characters/player/dash02.png",
        "dash4": "./CelesteSprites/Atlases/Gameplay/characters/player/dash03.png",
        #lookup
        "lookup1":"./CelesteSprites/Atlases/Gameplay/characters/player/lookUp00.png",
        "lookup2":"./CelesteSprites/Atlases/Gameplay/characters/player/lookUp01.png",
        "lookup3":"./CelesteSprites/Atlases/Gameplay/characters/player/lookUp02.png",
        "lookup4":"./CelesteSprites/Atlases/Gameplay/characters/player/lookUp03.png",
        "lookup5":"./CelesteSprites/Atlases/Gameplay/characters/player/lookUp04.png",
        "lookup6":"./CelesteSprites/Atlases/Gameplay/characters/player/lookUp05.png",
        "lookup7":"./CelesteSprites/Atlases/Gameplay/characters/player/lookUp06.png",
        "lookup8":"./CelesteSprites/Atlases/Gameplay/characters/player/lookUp07.png",
    }
    spritesLocationBadeline={
        #respawn sprite
        "respawn1":"./CelesteSprites/Atlases/Gameplay/characters/badeline/idle00.png",
        #wallhug sprite
        "wallhug1": "./CelesteSprites/Atlases/Gameplay/characters/badeline/climb00.png",

        #default idle animation
        "idle1": "./CelesteSprites/Atlases/Gameplay/characters/badeline/idle00.png",
        "idle2": "./CelesteSprites/Atlases/Gameplay/characters/badeline/idle01.png",
        "idle3": "./CelesteSprites/Atlases/Gameplay/characters/badeline/idle02.png",
        "idle4": "./CelesteSprites/Atlases/Gameplay/characters/badeline/idle03.png",
        "idle5": "./CelesteSprites/Atlases/Gameplay/characters/badeline/idle04.png",
        "idle6": "./CelesteSprites/Atlases/Gameplay/characters/badeline/idle05.png",
        "idle7": "./CelesteSprites/Atlases/Gameplay/characters/badeline/idle06.png",
        "idle8": "./CelesteSprites/Atlases/Gameplay/characters/badeline/idle07.png",

        #Walking right
        "walk1": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast00.png",
        "walk2": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast01.png",
        "walk3": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast02.png",
        "walk4": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast03.png",
        "walk5": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast04.png",
        "walk6": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast05.png",
        "walk7": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast06.png",
        "walk8": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast07.png",
        "walk9": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast08.png",
        "walk10": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast09.png",
        "walk11": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast10.png",
        "walk12": "./CelesteSprites/Atlases/Gameplay/characters/badeline/runFast11.png",
        

        #turning left
        "turn1": "./CelesteSprites/Atlases/Gameplay/characters/badeline/flip00.png",
        "turn2": "./CelesteSprites/Atlases/Gameplay/characters/badeline/flip01.png",
        "turn3": "./CelesteSprites/Atlases/Gameplay/characters/badeline/flip02.png",
        "turn4": "./CelesteSprites/Atlases/Gameplay/characters/badeline/flip03.png",
        "turn5": "./CelesteSprites/Atlases/Gameplay/characters/badeline/flip04.png",
        "turn6": "./CelesteSprites/Atlases/Gameplay/characters/badeline/flip05.png",
        "turn7": "./CelesteSprites/Atlases/Gameplay/characters/badeline/flip06.png",
        "turn8": "./CelesteSprites/Atlases/Gameplay/characters/badeline/flip07.png",


        #crouch
        "crouch1": "./CelesteSprites/Atlases/Gameplay/characters/badeline/duck.png",
        "crouch2": "./CelesteSprites/Atlases/Gameplay/characters/badeline/duck.png",
        "crouch3": "./CelesteSprites/Atlases/Gameplay/characters/badeline/duck.png",
        "crouch4": "./CelesteSprites/Atlases/Gameplay/characters/badeline/duck.png",

        #jump
        "jump1": "./CelesteSprites/Atlases/Gameplay/characters/badeline/jumpFast00.png",
        "jump2": "./CelesteSprites/Atlases/Gameplay/characters/badeline/jumpFast01.png",

        #falling
        "falling1": "./CelesteSprites/Atlases/Gameplay/characters/badeline/jumpFast02.png",
        "falling2": "./CelesteSprites/Atlases/Gameplay/characters/badeline/jumpFast03.png",

        #dash
        "dash1": "./CelesteSprites/Atlases/Gameplay/characters/badeline/dash00.png",
        "dash2": "./CelesteSprites/Atlases/Gameplay/characters/badeline/dash01.png",
        "dash3": "./CelesteSprites/Atlases/Gameplay/characters/badeline/dash02.png",
        "dash4": "./CelesteSprites/Atlases/Gameplay/characters/badeline/dash03.png",
        #lookup
        "lookup1":"./CelesteSprites/Atlases/Gameplay/characters/badeline/lookUp00.png",
        "lookup2":"./CelesteSprites/Atlases/Gameplay/characters/badeline/lookUp01.png",
        "lookup3":"./CelesteSprites/Atlases/Gameplay/characters/badeline/lookUp02.png",
        "lookup4":"./CelesteSprites/Atlases/Gameplay/characters/badeline/lookUp03.png",
        "lookup5":"./CelesteSprites/Atlases/Gameplay/characters/badeline/lookUp04.png",
        "lookup6":"./CelesteSprites/Atlases/Gameplay/characters/badeline/lookUp05.png",
        "lookup7":"./CelesteSprites/Atlases/Gameplay/characters/badeline/lookUp06.png",
        "lookup8":"./CelesteSprites/Atlases/Gameplay/characters/badeline/lookUp07.png",
    }

class DashResetEntityStuff:
    sprites ={"idle1":"idle2","idle2":"idle3","idle3":"idle4","idle4":"idle1",
                "flash1":"flash2","flash2":"flash3","flash3":"flash4","flash4":"idle1",
                "outline1":"outline1"
                }
    states = ["idle","flash","outline"]
    spritesLocation = {
        "idle1": "./CelesteSprites/Atlases/Gameplay/objects/refill/idle00.png",
        "idle2": "./CelesteSprites/Atlases/Gameplay/objects/refill/idle01.png",
        "idle3": "./CelesteSprites/Atlases/Gameplay/objects/refill/idle02.png",
        "idle4": "./CelesteSprites/Atlases/Gameplay/objects/refill/idle03.png",
        "flash1": "./CelesteSprites/Atlases/Gameplay/objects/refill/flash00.png",
        "flash2": "./CelesteSprites/Atlases/Gameplay/objects/refill/flash01.png",
        "flash3": "./CelesteSprites/Atlases/Gameplay/objects/refill/flash02.png",
        "flash4": "./CelesteSprites/Atlases/Gameplay/objects/refill/flash03.png",
        "outline1": "./CelesteSprites/Atlases/Gameplay/objects/refill/outline.png",
    }

class StawberryStuff:
    #get has 14 sprites
    sprites ={"idle1":"idle2","idle2":"idle3","idle3":"idle4","idle4":"idle5","idle5":"idle6","idle6":"idle7","idle7":"idle1",
              "collected1": "collected2","collected2":"collected3","collected3":"collected4","collected4":"collected5","collected5":"collected6","collected6":"collected7","collected7":"collected8","collected8":"collected9","collected9":"collected10","collected10":"collected11","collected11":"collected12","collected12":"collected13","collected13":"collected14","collected14":"end",
              "hidden1":"hidden1"
              }
    states = ["idle","get","hidden"]
    spritesLocation = {
        "idle1": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal00.png",
        "idle2": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal01.png",
        "idle3": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal02.png",
        "idle4": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal03.png",
        "idle5": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal04.png",
        "idle6": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal05.png",
        "idle7": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal06.png",

        "collected1": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal07.png",
        "collected2": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal08.png",
        "collected3": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal09.png",
        "collected4": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal10.png",
        "collected5": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal11.png",
        "collected6": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal12.png",
        "collected7": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal13.png",
        "collected8": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal14.png",
        "collected9": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal15.png",
        "collected10": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal16.png",
        "collected11": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal17.png",
        "collected12": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal18.png",
        "collected13": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal19.png",
        "collected14": "./CelesteSprites/Atlases/Gameplay/collectables/strawberry/normal20.png",


    }
class SpringStuff:
    sprites ={"idle1":"idle1",
                "extended1":"extended2","extended2":"extended3","extended3":"extended4","extended4":"extended5","extended5":"end",
                }
    states = ["idle","extended"]
    spritesLocation = {
        "idle1": "./CelesteSprites/Atlases/Gameplay/objects/spring/00.png",
        "extended1": "./CelesteSprites/Atlases/Gameplay/objects/spring/01.png",
        "extended2": "./CelesteSprites/Atlases/Gameplay/objects/spring/02.png",
        "extended3": "./CelesteSprites/Atlases/Gameplay/objects/spring/03.png",
        "extended4": "./CelesteSprites/Atlases/Gameplay/objects/spring/04.png",
        "extended5": "./CelesteSprites/Atlases/Gameplay/objects/spring/05.png",
    }
    spritesImageCrop= {
        "idle1": (2,13,12,3),
        "extended1": (2,7,12,9),
        "extended2": (2,5,12,10),
        "extended3": (2,7,12,9),
        "extended4": (2,9,12,7),
        "extended5": (2,12,12,4),
    }
    spritesOffset={
        "idle1": (5,37),
        "extended1": (5,20),
        "extended2": (5,10),
        "extended3": (5,20),
        "extended4": (5,25),
        "extended5": (5,30),
    }
class SpikeStuff:
    sprites ={"idle1":"idle1"}
    states = ["idle"]
    spritesLocation = {
        "idle1": "./CelesteSprites/Atlases/Gameplay/danger/spikes/outline_up00.png",
    }

class jumpParticles:
    firstSprite = "jumpParticle1"
    sprites = {"jumpParticle1":"jumpParticle2","jumpParticle2":"jumpParticle3","jumpParticle3":"jumpParticle1"}
    spritesLocation = {
        "jumpParticle1": "./atlas.png",
        "jumpParticle2": "./atlas.png",
        "jumpParticle3": "./atlas.png",
    }
    spritesImageCrop= {
        "jumpParticle1": (105,9, 6,6),
        "jumpParticle2": (112,9, 7,7),
        "jumpParticle3": (120,8, 8,8),
    }

class fallingBlockStuff:
    firstSpriteID = "idle1"
    states = ["idle","outline"]
    sprites= {"idle1":"idle1","outline1":"outline1"}
    spritesLocation = {
        "idle1": "./CelesteSprites/Atlases/Gameplay/objects/crumbleBlock/default.png",
        "outline1": "./CelesteSprites/Atlases/Gameplay/objects/crumbleBlock/outline.png",
    }