from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
from src.Items.Debuff import Debuff
import random as rd
import math

class Ka(Enemy):
    def __init__(self,name,health,damage,armor = 5):
        super().__init__(health,damage,armor,name='Ka',weakness=[])
        self.attacks = {'normal':[self.lice],'dot':[self.freaky]}
        self.gold = 1


    def lice(self,target):
        target.damageEnemy(self.damage)
        self.health += self.health // 2
        print(f'Ka gave you lice!')
    
    def freaky(self,target):
        if target.damage > 1:
            target.damage -= 1
            print(f'Ka is freaky!')



