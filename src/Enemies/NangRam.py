from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
from src.Items.Debuff import Debuff
import math

class NangRam(Enemy):
    def __init__(self,name,health,damage,armor = 0):
        super().__init__(health,damage,armor,name='NangRam',weakness=[])
        self.attacks = {'normal':[self.choke,self.royalDancer],'dot':[self.smile]}
        # self.attacks = {'normal':[self.smile],'dot':[self.smile]}
        self.gold = 4
    def choke(self,target):
        target.damageEnemy(self.damage)
        print(f'Nang Ram used choke!')

    def smile(self,target):
        target.damageEnemy(self.damage)
        def apply_no_card(target):
            target.noCard = True

        def remove_no_card(target):
            target.noCard = False

        no_melee_debuff = Debuff(name="No Card", apply_effect=apply_no_card, remove_effect=remove_no_card, duration=2)
        if no_melee_debuff.name not in [i.name for i in target.buffs]:
        
            target.buffs.append(no_melee_debuff)
            print(f'Nang Ram used Smile!')
        else:
            print('Nang Ram used Choke!')
    def royalDancer(self,target):
        if self.useUlt < 2:
            self.damage *= 2
            self.useUlt += 1
