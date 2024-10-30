class StatusEffect:
    def __init__(self, name, damage_per_turn, duration):
        self.name = name
        self.damage_per_turn = damage_per_turn
        self.duration = duration

    def apply(self, target):
        if self.duration > 0:
            target.damageEnemy(self.damage_per_turn)  
            self.duration -= 1  
