import pygame

class PlayerStuff:
    #idle has 8 sprites
    #jump has ? sprites ( not done)
    #walkRight has 12 sprites
    #walkLeft has 12 sprites
    #turning has 6 sprites
    #turning fast has 9 (not done)
    #crouch has 4 sprites
    sprites = {"idle1":"idle2","idle2":"idle3","idle3":"idle4","idle4":"idle5","idle5":"idle6","idle6":"idle7","idle7":"idle8","idle8":"idle1",
                "walkRight1":"walkRight2","walkRight2":"walkRight3","walkRight3":"walkRight4","walkRight4":"walkRight5","walkRight5":"walkRight6","walkRight6":"walkRight7","walkRight7":"walkRight8","walkRight8":"walkRight9","walkRight9":"walkRight10","walkRight10":"walkRight11","walkRight11":"walkRight12","walkRight12":"walkRight1",
                "walkLeft1":"walkLeft2","walkLeft2":"walkLeft3","walkLeft3":"walkLeft4","walkLeft4":"walkLeft5","walkLeft5":"walkLeft6","walkLeft6":"walkLeft7","walkLeft7":"walkLeft8","walkLeft8":"walkLeft9","walkLeft9":"walkLeft10","walkLeft10":"walkLeft11","walkLeft11":"walkLeft12","walkLeft12":"walkLeft1",
                "turningLeft1":"turningLeft2","turningLeft2":"turningLeft3","turningLeft3":"turningLeft4","turningLeft4":"turningLeft5","turningLeft5":"turningLeft6","turningLeft6":"turningLeft7","turningLeft7":"turningLeft8","turningLeft8":"end",
                "turningRight1":"turningRight2","turningRight2":"turningRight3","turningRight3":"turningRight4","turningRight4":"turningRight5","turningRight5":"turningRight6","turningRight6":"turningRight7","turningRight7":"turningRight8","turningRight8":"end",
                "crouch1":"crouch2","crouch2":"crouch3","crouch3":"crouch4","crouch4":"crouch1",
                "jump1":"jump2","jump2":"jump3","jump3":"jump4","jump4":"jump1"
               }
    
    statesInit = {"idle":"idle1","jump":"jump1","walkRight":"walkRight1","walkLeft":"walkLeft1","crouch":"crouch1","turningLeft":"turningLeft1","turningRight":"turningRight1"}
    states = ["idle","jump","walkRight","walkLeft","crouch","turningLeft","turningRight"]

    statesMovement = {"idle":(0,0),"jump":(0,-1),"walkRight":(1,0),"walkLeft":(-1,0),"crouch":(0,1),"turningLeft":(-1,0),"turningRight":(1,0)}

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
