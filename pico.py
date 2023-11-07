def paused():
    pass

def touchingSpikes():
    pass

def harakiri():
    pass

def onGround():
    pass

def smoke():
    pass

HEIGHT     = 800
JUMPFRAMES = 5

#x, jump
vector = [0, True]
wasOnGround = False
y = 0
previousJump = False
jumpFrames = JUMPFRAMES
def update():
    if paused():
        return
    # right == 1, left == -1, neither == 0
    pInput = vector[0]


    if touchingSpikes() or y>HEIGHT:
        #kill thyself tarnished
        harakiri()


    if onGround() and not wasOnGround:
        #landed
        smoke()
    
    jump = vector[1] and not previousJump
    previousJump = vector[1]

    if jump:
        jumpFrames = JUMPFRAMES
    elif jumpFrames>0:
        jumpFrames-=1
