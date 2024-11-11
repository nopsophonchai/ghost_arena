from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
import math

class GongGoi(Enemy):
    def __init__(self,name,health,damage,armor = 0):
        super().__init__(health,damage,armor,name='GongGoi',weakness=['Fire','Rice'])
        self.attacks = {'normal':[self.kick],'dot':[self.ultimate]}
        self.gold = 3
    def kick(self,target):
        target.damageEnemy(self.damage)
        print(f'GongGoi used kick!')

    def ultimate(self,target):
        poison = StatusEffect('poison',math.ceil(self.damage/2),2)
        target.statusEffects.append(poison)
        print(f'GongGoi used poison!')