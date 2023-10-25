



class State:
    def __init__(self, name):
        self.name = name

    def enter(self):
        pass
    
    def exit(self):
        pass
    
    def update(self,object):
        pass
    

class Transition:
    def __init__(self, from_state, to_state):
        self.from_state = from_state
        self.to_state = to_state