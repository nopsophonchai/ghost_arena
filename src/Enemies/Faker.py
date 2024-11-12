from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
from src.Items.Debuff import Debuff
import random as rd
import math

class Faker(Enemy):
    def __init__(self,name,health,damage,armor = 10):
        super().__init__(health,damage,armor,name='Faker',weakness=[])
        self.attacks = {'normal':[self.smile,self.lice,self.freaky,self.poison,self.royalDancer,self.bigHand,self.epred],'dot':[self.smile]}
        self.gold = 1000


    def lice(self,target):
        target.damageEnemy(self.damage)
        self.health += self.health // 2
        print(f'Faker gave you lice!')
    
    def freaky(self,target):
        if target.damage > 1:
            target.damage -= 1
            print(f'Faker is freaky!')

    def poison(self,target):
        poison = StatusEffect('poison',math.ceil(self.damage/2),2)
        target.statusEffects.append(poison)
        print(f'Faker used poison!')

    def smile(self,target):
        target.damageEnemy(self.damage)
        def apply_no_card(target):
            target.noCard = True

        def remove_no_card(target):
            target.noCard = False

        no_melee_debuff = Debuff(name="No Card", apply_effect=apply_no_card, remove_effect=remove_no_card, duration=2)
        if no_melee_debuff.name not in [i.name for i in target.buffs]:
        
            target.buffs.append(no_melee_debuff)
            print(f'Faker used Smile!')
        else:
            print('Faker used Choke!')

    def royalDancer(self,target):
        if self.useUlt < 2:
            self.damage *= 2
            self.useUlt += 1
            print('Faker dances')


    def bigHand(self,target):
        target.damageEnemy(self.damage)
        def apply_no_melee(target):
            target.noMelee = True

        def remove_no_melee(target):
            target.noMelee = False

        no_melee_debuff = Debuff(name="No Melee", apply_effect=apply_no_melee, remove_effect=remove_no_melee, duration=2)
        target.buffs.append(no_melee_debuff)
        print(f'Faker used big hand!')

    def epred(self,target):
        target.damageEnemy(self.damage + 2)
        def apply_no_armor(target):
            target.noArmor = True
        def remove_no_armor(target):
            target.noArmor = False
        
        no_armor_debuff = Debuff(name="No Armor", apply_effect=apply_no_armor, remove_effect=remove_no_armor, duration= 2)
        target.buffs.append(no_armor_debuff)
        print(f'Faker epred!')


