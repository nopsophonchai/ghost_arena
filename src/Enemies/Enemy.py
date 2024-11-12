import pygame
import random as rd


class Enemy:
    def __init__(self,health,damage,armor,name,immune = [],weakness = []):
        self.maxHealth = health
        self.health = health
        self.damage = damage
        self.armor = armor
        self.name = name
        self.statusEffects = []
        self.attacks = {}
        self.isDead = False
        self.miss = False
        self.buffs = []
        self.immune = immune
        self.weakness = weakness
        self.useUlt = 0
    

    def damageEnemy(self,damage,type = 'normal'):
        if type in self.immune:
            pass
        elif type == 'normal' or (type not in self.weakness and type not in self.immune):
            print('Not Weak!')
            self.health -= max((damage - self.armor),0)
        elif type == 'true':
            self.health -= damage
        elif type in self.weakness:
            print('Weak!')
            self.health -= int(1.5* damage)

    def chooseAttacks(self):
        attackType, attackList = rd.choice(list(self.attacks.items()))

        return (attackType,attackList)

    def attack(self,target):
        print(f'Current Miss: {self.miss}')
        if not self.miss:
            payload = self.chooseAttacks()
            chosenType = payload[0]
            chosenList = payload[1]
            chosenAttack = rd.choice(chosenList)
            
            if chosenType == 'normal':
                chosenAttack(target)
            elif chosenType == 'dot': #Code looks dumb now, might change later
                chosenAttack(target)


    def applyStatEff(self):
        for i in self.statusEffects:
            i.apply(self)
            if self.health <= 0:
                self.isDead = True
            if i.duration <= 0:
                self.statusEffects.remove(i)

    def applyDebuffs(self):
            print(self.buffs)
            for debuff in self.buffs[:]: 
                debuff.apply(self)
                print(self.miss)
                if debuff.duration <= 0:

                    debuff.remove(self)  
                    self.buffs.remove(debuff)
                    print(self.miss)

    