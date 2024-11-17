from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
from src.Items.Debuff import Debuff
import random as rd
import math
from src.constants import *

class Ka(Enemy):
    def __init__(self,name,health,damage,armor = 5):
        super().__init__(health,damage,armor,name='Ka',weakness=[])
        self.attacks = {'normal':[(self.lice,'lice',f'Heals itself for {self.health//2}\nDeal {self.damage} damage')],'dot':[(self.freaky,'freaky',f'Reduce your damage by 1\nIf you have 6 damage\nor lower, deal {self.damage} damage\n\nNo immunity or weakness')]}
        self.gold = 1


    def lice(self,target):
        target.damageEnemy(self.damage)
        self.health += self.health // 2
        print(f'Ka gave you lice!')
    
    def freaky(self,target):
        if target.damage > 6:
            target.damage -= 1
            print(f'Ka is freaky!')
            print([i[0] for i in target.statusList])
            if 'Decrease Damage' not in [i[0] for i in target.statusList]:
                print('FREAKKKKK')
                target.statusList.append(('Decrease Damage','graphics/icons/decrease.png'))
        else:
            target.damageEnemy(self.damage)



