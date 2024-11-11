class StatusEffect:
    def __init__(self, name, damage_per_turn, duration,damageType='normal'):
        self.name = name
        self.damage_per_turn = damage_per_turn
        self.duration = duration
        self.damageType = damageType

    def apply(self, target):
        if self.duration > 0:
            target.damageEnemy(self.damage_per_turn,self.damageType)  
            self.duration -= 1  
