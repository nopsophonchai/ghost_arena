from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
import math
from src.constants import *

class Krasue(Enemy):
    def __init__(self,name,health,damage,armor = 0):
        super().__init__(health,damage,armor,name='Krasue',immune=['normal'],weakness=['Rice'])
        self.attacks = {'normal':[(self.spit,'spit')],'dot':[(self.ultimate,'intestine beam')]}
        self.gold = 4
    def spit(self,target):
        target.damageEnemy(self.damage)
        print(f'Krasue used spit!')

    def ultimate(self,target):
        target.damageEnemy(self.damage,'true')
        print(f'Phrai used poison!')