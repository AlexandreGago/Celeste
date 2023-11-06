class Actor:
    def __init__(self,x,y,height,width,serviceLocator) -> None:
        self.observers = []
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.serviceLocator = serviceLocator

    def move(self):
        raise NotImplementedError()
    
    def add_observer(self,observer):
        self.observers.append(observer)

    def remove_observer(self,observer):
        self.observers.remove(observer)

    def notify(self,entity,event):
        raise NotImplementedError()
    