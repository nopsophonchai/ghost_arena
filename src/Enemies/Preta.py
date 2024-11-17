from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
from src.Items.Debuff import Debuff
from src.constants import *

import math

class Preta(Enemy):
    def __init__(self,name,health,damage,armor = 0):
        super().__init__(health,damage,armor,name='Preta',weakness=['Fire','Rice','Water'])
        self.attacks = {'normal':[(self.scream,'scream',f'Deal {self.damage} damage')],'dot':[(self.epred,'E Pred',f'Deal {self.damage+2} damage\nRemove your armor\nfor 1 turn'),(self.bigHand,'Big Hand',f'Deal {self.damage} damage\nDisable sword for 1 turn\n\nWeak to Fire, Rice, and Water')]}
        self.gold = 4
        

    def scream(self,target):
        target.damageEnemy(self.damage)
        print(f'Preta used scream!')
        # target.addEffect('GongGoi used kick!', (WIDTH / 3, HEIGHT / 6), duration=100)

    def bigHand(self,target):
        target.damageEnemy(self.damage)
        def apply_no_melee(target):
            target.noMelee = True

        def remove_no_melee(target):
            target.noMelee = False

        no_melee_debuff = Debuff(name="No Melee", apply_effect=apply_no_melee, remove_effect=remove_no_melee, duration=2)
        target.buffs.append(no_melee_debuff)
        target.statusList.append(('No Melee','graphics/icons/noMelee.png'))
        print(f'Preta used big hand!')

    def epred(self,target):
        target.damageEnemy(self.damage + 2)
        def apply_no_armor(target):
            target.noArmor = True
        def remove_no_armor(target):
            target.noArmor = False
        
        no_armor_debuff = Debuff(name="No Armor", apply_effect=apply_no_armor, remove_effect=remove_no_armor, duration= 2)
        target.buffs.append(no_armor_debuff)
        target.statusList.append(('No Armor','graphics/icons/noArmor.png'))
        print(f'Preta epred!')


