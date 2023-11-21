class Actor:
    def __init__(self,x:int,y:int,height:int,width:int,serviceLocator=None) -> None:
        """
        Initializes an actor

        Args:
            x (int): x position of the actor
            y (int): y position of the actor
            height (int): height of the actor
            width (int): width of the actor
            serviceLocator (ServiceLocator): ServiceLocator object (default: None)

        Returns:
            None
        """

        self.observers = []
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.serviceLocator = serviceLocator

    def move(self):
        raise NotImplementedError()
    
    def add_observer(self,observer):
        """
        Adds an observer to the actor

        Args:
            observer (Observer): observer to be added

        Returns:
            None
        """
        self.observers.append(observer)

    def remove_observer(self,observer):
        self.observers.remove(observer)

    def notify(self,entity,event):
        raise NotImplementedError()
    