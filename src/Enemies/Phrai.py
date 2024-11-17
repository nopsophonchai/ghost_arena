from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
import math
from src.constants import *

class Phrai(Enemy):
    def __init__(self,name,health,damage,armor = 0):
        super().__init__(health,damage,armor,name='Phrai',immune=['normal','Water'],weakness=['Fire','Rice'])
        self.attacks = {'normal':[(self.hair,'hair')],'dot':[(self.ultimate,'saen sap')]}
        self.gold = 4
    def hair(self,target):
        target.damageEnemy(self.damage)
        print(f'Phrai used hair!')

    def ultimate(self,target):
        poison = StatusEffect('poison',self.damage,3)
        target.statusEffects.append(poison)
        target.statusList.append(('poison','graphics/icons/poison.png'))
        print(f'Phrai used poison!')