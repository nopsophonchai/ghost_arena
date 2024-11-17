from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
import math
from src.constants import *

class GongGoi(Enemy):
    def __init__(self,name,health,damage,armor = 0):
        super().__init__(health,damage,armor,name='GongGoi',weakness=['Fire','Rice'])
        self.attacks = {'normal':[(self.kick,'kick',f'Deal {self.damage} damage')],'dot':[(self.ultimate,'poison',f'Deal {math.ceil(self.damage/2)} poison damage\nfor 2 turns\n\nWeakness: Fire,Rice')]}
        self.gold = 3
    def kick(self,target):
        target.damageEnemy(self.damage)
        print(f'GongGoi used kick!')
        # target.addEffect('GongGoi used kick!', (WIDTH / 3, HEIGHT / 6), duration=100)

    def ultimate(self,target):
        poison = StatusEffect('poison',math.ceil(self.damage/2),2)
        target.statusEffects.append(poison)
        target.statusList.append(('poison','graphics/icons/poison.png'))
        print(f'GongGoi used poison!')
        # target.addEffect('GongGoi used poison!', (WIDTH / 3, HEIGHT / 6), duration=100)