
class StateMachine:
    def __init__(self):
        self.current = None

    def Change(self, state_name, enter_params):
        assert(self.states[state_name]) 
        if self.current:
            self.current.Exit()
        self.current = self.states[state_name]
        self.current.Enter(enter_params)

    def update(self, dt, events):
        self.current.update(dt, events)

    def render(self):
        self.current.render(self.screen)

    def SetScreen(self, screen):
        self.screen = screen

    def SetStates(self, states):
        self.states = states
        print(f"States Set, {states}")
    
    def Reset(self):
        for state in self.states.values():
            if hasattr(state, "Reset"):
                state.Reset()  
        print(self.states)