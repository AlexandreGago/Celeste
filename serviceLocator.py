class ServiceLocator:
    _instance = None

    def __new__(cls):
        if cls._instance is not None:
            raise ValueError("An instance of ServiceLocator already exists")
        cls._instance = super(ServiceLocator, cls).__new__(cls)
        return cls._instance
        
    def __init__(self) -> None:
        self.inputHandler = None
        self.players = []
        self.map = None
        self.display = None
        self.actorList = []
        self.fallingBlocks = []
        self.clouds = []
        self.offset = None
        self.screenshake = None
        self.score = 0


    def getPlayers(self):
        return self.players

    def getInputHandler(self):
        return self.inputHandler

    def getDisplay(self):
        return self.display
