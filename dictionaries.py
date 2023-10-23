import pygame

class PlayerStuff:
    #idle has 8 sprites
    #jump has ? sprites ( not done)
    #walkRight has 12 sprites
    #walkLeft has 12 sprites
    #turning has 6 sprites
    #turning fast has 9 (not done)
    #crouch has 4 sprites
    sprites = {
        "idle1":"idle2","idle2":"idle3","idle3":"idle4","idle4":"idle5","idle5":"idle6","idle6":"idle7","idle7":"idle8","idle8":"idle1",
        "walkRight1":"walkRight2","walkRight2":"walkRight3","walkRight3":"walkRight4","walkRight4":"walkRight5","walkRight5":"walkRight6","walkRight6":"walkRight7","walkRight7":"walkRight8","walkRight8":"walkRight9","walkRight9":"walkRight10","walkRight10":"walkRight11","walkRight11":"walkRight12","walkRight12":"walkRight1",
        "walkLeft1":"walkLeft2","walkLeft2":"walkLeft3","walkLeft3":"walkLeft4","walkLeft4":"walkLeft5","walkLeft5":"walkLeft6","walkLeft6":"walkLeft7","walkLeft7":"walkLeft8","walkLeft8":"walkLeft9","walkLeft9":"walkLeft10","walkLeft10":"walkLeft11","walkLeft11":"walkLeft12","walkLeft12":"walkLeft1",
        "turningLeft1":"turningLeft2","turningLeft2":"turningLeft3","turningLeft3":"turningLeft4","turningLeft4":"turningLeft5","turningLeft5":"turningLeft6","turningLeft6":"turningLeft7","turningLeft7":"turningLeft8","turningLeft8":"end",
        "turningRight1":"turningRight2","turningRight2":"turningRight3","turningRight3":"turningRight4","turningRight4":"turningRight5","turningRight5":"turningRight6","turningRight6":"turningRight7","turningRight7":"turningRight8","turningRight8":"end",
        "crouch1":"crouch2","crouch2":"crouch3","crouch3":"crouch4","crouch4":"crouch1",
        "jump1":"jump2","jump2":"jump3","jump3":"jump4","jump4":"jump1"
    }
    spritesHairOffset = {"idle":{"idle1":(0,5),"idle2":(0,5),"idle3":(0,5),"idle4":(0,5),"idle5":(0,0),"idle6":(0,0),"idle7":(0,0),"idle8":(0,0)},
                        "walkRight":{"walkRight1":(0,0),"walkRight2":(0,0),"walkRight3":(0,0),"walkRight4":(0,0),"walkRight5":(0,0),"walkRight6":(0,0),"walkRight7":(0,0),"walkRight8":(0,0),"walkRight9":(0,0),"walkRight10":(0,0),"walkRight11":(0,0),"walkRight12":(0,0)},
                        "walkLeft":{"walkLeft1":(0,0),"walkLeft2":(0,0),"walkLeft3":(0,0),"walkLeft4":(0,0),"walkLeft5":(0,0),"walkLeft6":(0,0),"walkLeft7":(0,0),"walkLeft8":(0,0),"walkLeft9":(0,0),"walkLeft10":(0,0),"walkLeft11":(0,0),"walkLeft12":(0,0)},
                        "turningLeft":{"turningLeft1":(0,0),"turningLeft2":(0,0),"turningLeft3":(0,0),"turningLeft4":(0,0),"turningLeft5":(0,0),"turningLeft6":(0,0),"turningLeft7":(0,0),"turningLeft8":(0,0)},
                        "turningRight":{"turningRight1":(0,0),"turningRight2":(0,0),"turningRight3":(0,0),"turningRight4":(0,0),"turningRight5":(0,0),"turningRight6":(0,0),"turningRight7":(0,0),"turningRight8":(0,0)},
                        "crouch":{"crouch1":(0,0),"crouch2":(0,0),"crouch3":(0,0),"crouch4":(0,0)},
                        "jump":{"jump1":(0,0),"jump2":(0,0),"jump3":(0,0),"jump4":(0,0)}
                        }
    states = ["idle","jump","walkRight","walkLeft","crouch","turningLeft","turningRight"]


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
    }
