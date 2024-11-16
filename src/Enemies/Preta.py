from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
from src.Items.Debuff import Debuff

import math

class Preta(Enemy):
    def __init__(self,name,health,damage,armor = 0):
        super().__init__(health,damage,armor,name='Preta',weakness=['Fire','Rice','Water'])
        self.attacks = {'normal':[self.scream],'dot':[self.epred,self.bigHand]}
        self.gold = 4
        

    def scream(self,target):
        target.damageEnemy(self.damage)
        print(f'Preta used scream!')

    def bigHand(self,target):
        target.damageEnemy(self.damage)
        def apply_no_melee(target):
            target.noMelee = True

        def remove_no_melee(target):
            target.noMelee = False

        no_melee_debuff = Debuff(name="No Melee", apply_effect=apply_no_melee, remove_effect=remove_no_melee, duration=2)
        target.buffs.append(no_melee_debuff)
        print(f'Preta used big hand!')

    def epred(self,target):
        target.damageEnemy(self.damage + 2)
        def apply_no_armor(target):
            target.noArmor = True
        def remove_no_armor(target):
            target.noArmor = False
        
        no_armor_debuff = Debuff(name="No Armor", apply_effect=apply_no_armor, remove_effect=remove_no_armor, duration= 2)
        target.buffs.append(no_armor_debuff)
        print(f'Preta epred!')


