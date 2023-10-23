import pygame

class PlayerStuff:
    #idle has 8 sprites
    #jump has ? sprites ( not done)
    #walkRight has 12 sprites
    #walkLeft has 12 sprites
    #turning has 6 sprites
    #turning fast has 9 (not done)
    #crouch has 4 sprites
    #dash has 4 sprites
    sprites = {
        "idle1":"idle2","idle2":"idle3","idle3":"idle4","idle4":"idle5","idle5":"idle6","idle6":"idle7","idle7":"idle8","idle8":"idle1",
        "walkRight1":"walkRight2","walkRight2":"walkRight3","walkRight3":"walkRight4","walkRight4":"walkRight5","walkRight5":"walkRight6","walkRight6":"walkRight7","walkRight7":"walkRight8","walkRight8":"walkRight9","walkRight9":"walkRight10","walkRight10":"walkRight11","walkRight11":"walkRight12","walkRight12":"walkRight1",
        "walkLeft1":"walkLeft2","walkLeft2":"walkLeft3","walkLeft3":"walkLeft4","walkLeft4":"walkLeft5","walkLeft5":"walkLeft6","walkLeft6":"walkLeft7","walkLeft7":"walkLeft8","walkLeft8":"walkLeft9","walkLeft9":"walkLeft10","walkLeft10":"walkLeft11","walkLeft11":"walkLeft12","walkLeft12":"walkLeft1",
        "turningLeft1":"turningLeft2","turningLeft2":"turningLeft3","turningLeft3":"turningLeft4","turningLeft4":"turningLeft5","turningLeft5":"turningLeft6","turningLeft6":"turningLeft7","turningLeft7":"turningLeft8","turningLeft8":"end",
        "turningRight1":"turningRight2","turningRight2":"turningRight3","turningRight3":"turningRight4","turningRight4":"turningRight5","turningRight5":"turningRight6","turningRight6":"turningRight7","turningRight7":"turningRight8","turningRight8":"end",
        "crouch1":"crouch2","crouch2":"crouch3","crouch3":"crouch4","crouch4":"crouch1",
        "jump1":"jump2","jump2":"jump3","jump3":"jump4","jump4":"jump1",
        "dash1":"dash2","dash2":"dash3","dash3":"dash4","dash4":"dash1"
    }

    spritesHairOffset = {"idle":{"idle1":(0,5),"idle2":(0,5),"idle3":(0,5),"idle4":(0,5),"idle5":(0,0),"idle6":(0,0),"idle7":(0,0),"idle8":(0,0)},
                        "walkRight":{"walkRight1":(5,5),"walkRight2":(5,0),"walkRight3":(5,0),"walkRight4":(5,0),"walkRight5":(5,10),"walkRight6":(5,5),"walkRight7":(5,0),"walkRight8":(5,0),"walkRight9":(5,0),"walkRight10":(5,0),"walkRight11":(5,10),"walkRight12":(5,5)},
                        "walkLeft":{"walkLeft1":(5,5),"walkLeft2":(5,0),"walkLeft3":(5,0),"walkLeft4":(5,0),"walkLeft5":(5,10),"walkLeft6":(5,5),"walkLeft7":(5,0),"walkLeft8":(5,0),"walkLeft9":(5,0),"walkLeft10":(5,0),"walkLeft11":(5,0),"walkLeft12":(5,10)},
                        "turningLeft":{"turningLeft1":(0,0),"turningLeft2":(0,0),"turningLeft3":(0,0),"turningLeft4":(0,0),"turningLeft5":(0,0),"turningLeft6":(0,0),"turningLeft7":(0,0),"turningLeft8":(0,0)},
                        "turningRight":{"turningRight1":(0,0),"turningRight2":(0,0),"turningRight3":(0,0),"turningRight4":(0,0),"turningRight5":(0,0),"turningRight6":(0,0),"turningRight7":(0,0),"turningRight8":(0,0)},
                        "crouch":{"crouch1":(0,0),"crouch2":(0,0),"crouch3":(0,0),"crouch4":(0,0)},
                        "jump":{"jump1":(5,10),"jump2":(5,10),"jump3":(0,10),"jump4":(-5,10)},
                        "dash":{"dash1":(10,0),"dash2":(10,0),"dash3":(10,0),"dash4":(10,0)},
                        }
    
    states = ["idle","jump","walkRight","walkLeft","crouch","turningLeft","turningRight"]
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

    spritesLocation={
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
        "walkRight1": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast00.png",
        "walkRight2": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast01.png",
        "walkRight3": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast02.png",
        "walkRight4": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast03.png",
        "walkRight5": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast04.png",
        "walkRight6": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast05.png",
        "walkRight7": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast06.png",
        "walkRight8": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast07.png",
        "walkRight9": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast08.png",
        "walkRight10": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast09.png",
        "walkRight11": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast10.png",
        "walkRight12": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast11.png",
        
        #walking left
        "walkLeft1": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast00.png",
        "walkLeft2": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast01.png",
        "walkLeft3": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast02.png",
        "walkLeft4": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast03.png",
        "walkLeft5": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast04.png",
        "walkLeft6": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast05.png",
        "walkLeft7": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast06.png",
        "walkLeft8": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast07.png",
        "walkLeft9": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast08.png",
        "walkLeft10": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast09.png",
        "walkLeft11": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast10.png",
        "walkLeft12": "./CelesteSprites/Atlases/Gameplay/characters/player/runFast11.png",

        #turning left
        "turningLeft1": "./CelesteSprites/Atlases/Gameplay/characters/player/flip00.png",
        "turningLeft2": "./CelesteSprites/Atlases/Gameplay/characters/player/flip01.png",
        "turningLeft3": "./CelesteSprites/Atlases/Gameplay/characters/player/flip02.png",
        "turningLeft4": "./CelesteSprites/Atlases/Gameplay/characters/player/flip03.png",
        "turningLeft5": "./CelesteSprites/Atlases/Gameplay/characters/player/flip04.png",
        "turningLeft6": "./CelesteSprites/Atlases/Gameplay/characters/player/flip05.png",
        "turningLeft7": "./CelesteSprites/Atlases/Gameplay/characters/player/flip06.png",
        "turningLeft8": "./CelesteSprites/Atlases/Gameplay/characters/player/flip07.png",



        #turning right
        "turningRight1": "./CelesteSprites/Atlases/Gameplay/characters/player/flip00.png",
        "turningRight2": "./CelesteSprites/Atlases/Gameplay/characters/player/flip01.png",
        "turningRight3": "./CelesteSprites/Atlases/Gameplay/characters/player/flip02.png",
        "turningRight4": "./CelesteSprites/Atlases/Gameplay/characters/player/flip03.png",
        "turningRight5": "./CelesteSprites/Atlases/Gameplay/characters/player/flip04.png",
        "turningRight6": "./CelesteSprites/Atlases/Gameplay/characters/player/flip05.png",
        "turningRight7": "./CelesteSprites/Atlases/Gameplay/characters/player/flip06.png",
        "turningRight8": "./CelesteSprites/Atlases/Gameplay/characters/player/flip07.png",


        #crouch
        "crouch1": "./CelesteSprites/Atlases/Gameplay/characters/player/duck.png",
        "crouch2": "./CelesteSprites/Atlases/Gameplay/characters/player/duck.png",
        "crouch3": "./CelesteSprites/Atlases/Gameplay/characters/player/duck.png",
        "crouch4": "./CelesteSprites/Atlases/Gameplay/characters/player/duck.png",

        #jump
        "jump1": "./CelesteSprites/Atlases/Gameplay/characters/player/jumpFast00.png",
        "jump2": "./CelesteSprites/Atlases/Gameplay/characters/player/jumpFast01.png",
        "jump3": "./CelesteSprites/Atlases/Gameplay/characters/player/jumpFast02.png",
        "jump4": "./CelesteSprites/Atlases/Gameplay/characters/player/jumpFast03.png",

        #dash
        "dash1": "./CelesteSprites/Atlases/Gameplay/characters/player/dash00.png",
        "dash2": "./CelesteSprites/Atlases/Gameplay/characters/player/dash01.png",
        "dash3": "./CelesteSprites/Atlases/Gameplay/characters/player/dash02.png",
        "dash4": "./CelesteSprites/Atlases/Gameplay/characters/player/dash03.png",

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