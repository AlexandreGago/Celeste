class ServiceLocator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceLocator, cls).__new__(cls)
            # Your initialization code here
            cls._instance.inputHandler = None
            cls._instance.players = []
            cls._instance.frameCount = None
            cls._instance.map = None
            cls._instance.display = None
            cls._instance.actorList = []
            cls._instance.fallingBlocks = []
            cls._instance.clouds = []
            cls._instance.offset = None
            cls._instance.screenshake = None
            cls._instance.score = 0
        return cls._instance

    def getPlayers(self):
        return self.players

    def getInputHandler(self):
        return self.inputHandler

    def getFrameCount(self):
        return self.frameCount

    def getDisplay(self):
        return self.display
