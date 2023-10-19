class Actor:
    def __init__(self) -> None:
        self.observers = []

    def move(self):
        raise NotImplementedError()
    
    def add_observer(self,observer):
        self.observers.append(observer)

    def remove_observer(self,observer):
        self.observers.remove(observer)

    def notify(self,entity,event):
        for obs in self.observers:
            obs.notify(entity,event)
    