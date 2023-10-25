from state import State,Transition

class Idle(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        
    def update(self,object):
        return super().update(object)

class Walk(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        
    def update(self,object):
        return super().update(object)

class Turning(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        
    def update(self,object):
        return super().update(object)

class Jump(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        
    def update(self,object):
        return super().update(object)
    
class Dash(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        
    def update(self,object):
        return super().update(object)

class Crouch(State):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        
    def update(self,object):
        return super().update(object)
    
class FSM:
    def __init__(self,states:list[State],transitions:dict[Transition])->None:
        self.states = states
        self.transitions = transitions 

        self.current:State = self.states[0]
        # self.end:State = self.states[-1]
    
    def update(self,event,object):
        if event:
            trans = None#self.transitions.get(event)
            if trans and trans.from_state == self.current:
                self.current.exit()
                self.current = trans.to_state
                self.current.enter()
        self.current.update(object)

        # if self.current == self.end:
        #     self.current.exit()
        #     return False
        return True