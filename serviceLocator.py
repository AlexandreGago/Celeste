class ServiceLocator():
    def __init__(self):
        self.inputHandler = None
        self.players = []
        self.frameCount = None
        self.map = None
        self.display = None
        self.actorList = []

        self.fallingBlocks = []
        self.clouds = []
        
        self.offset = None
        self.screenshake = None
    
    def getPlayers(self):
        return self.players
    
    def getInputHandler(self):
        return self.inputHandler
    
    def getFrameCount(self):
        return self.frameCount

    def getDisplay(self):
        return self.display