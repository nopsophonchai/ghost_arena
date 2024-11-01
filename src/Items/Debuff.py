class Debuff:
    def __init__(self, name, apply_effect, remove_effect, duration):
        self.name = name
        self.apply_effect = apply_effect 
        self.remove_effect = remove_effect  
        self.duration = duration

    def apply(self, target):
        if self.duration > 0:
            self.apply_effect(target)
            self.duration -= 1 

    def remove(self, target):
        self.remove_effect(target)
