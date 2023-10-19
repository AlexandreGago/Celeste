class ServiceLocator():
    def __init__(self):
        self.inputHandler = None
        self.player = None
        self.frameCount = None
        self.map = None
    
    def getPlayer(self):
        return self.player
    
    def getInputHandler(self):
        return self.inputHandler
    
    def getFrameCount(self):
        return self.frameCount