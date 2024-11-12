from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
from src.Items.Debuff import Debuff
import random as rd
import math

class Dang(Enemy):
    def __init__(self,name,health,damage,nak,armor = 0):
        super().__init__(health,damage,armor,name='Dang',weakness=[])
        self.attacks = {'normal':[self.dangAttack],'dot':[self.dangHeal]}
        self.gold = 1
        self.dangFlag = False
        self.nak = nak

    def dangAttack(self,target):
        target.damageEnemy(self.damage,'true')
        print(f'Dang Attacks!')
    
    def dangHeal(self,target):
        self.nak.health += self.damage


class MaeNak(Enemy):
    def __init__(self,name,health,damage,armor = 0):
        super().__init__(health,damage,armor,name='MaeNak',weakness=[])
        self.attacks = {'normal':[self.mothersScream],'dot':[self.summonDaeng]}
        # self.attacks = {'normal':[self.smile],'dot':[self.smile]}
        self.gold = 4
        self.dangFlag = False
        self.dangCool = 3

    def passive(self,target):
        if rd.random() > 0.5:
            if len(target.current) != 0:
                target.current.pop(rd.randint(0,len(target.current)-1))
    def mothersScream(self,target):
        self.passive(target)
        target.damageEnemy(self.damage,'true')
        print(f'Mae Nak used Mommy Scream!')

    def summonDaeng(self,target):
        self.passive(target)
        if self.dangCool == 3:
            self.dangFlag = True
            print('Dang is summoned')
            self.dangCool = 0
        else:
            self.dangCool += 1
            print(f'DangCool+ {self.dangCool}')
            self.mothersScream(target)