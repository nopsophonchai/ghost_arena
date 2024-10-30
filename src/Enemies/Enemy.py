import pygame
import random as rd


class Enemy:
    def __init__(self,health,damage,armor,name):
        self.health = health
        self.damage = damage
        self.armor = armor
        self.name = name
        self.statusEffects = []
        self.attacks = {}

    def damageEnemy(self,damage):
        self.health -= (damage - self.armor)

    def chooseAttacks(self):
        attackType, attackList = rd.choice(list(self.attacks.items()))

        return (attackType,attackList)

    def attack(self,target):
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
            if i.duration <= 0:
                self.statusEffects.remove(i)

    