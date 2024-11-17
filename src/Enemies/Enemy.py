import pygame
import random as rd
from src.resources import enemyAni
from src.constants import *

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

        self.currAni = None
        self.animationList = enemyAni

        self.effectList = []
        self.statusList = []
    

    def damageEnemy(self,damage,type = 'normal'):
        damageTaken = 0
        color = (153,153,153)
        if type in self.immune:
            pass
        elif type == 'normal' or (type not in self.weakness and type not in self.immune):
            print('Not Weak!')
            print(f'{damage} - {self.armor} = {damage - self.armor}')
            print(f'{self.health} - {damage - self.armor} = {self.health-(damage - self.armor)}')
            damageTaken = max((damage - self.armor),0)
            self.health -= damageTaken
            
            print('Animation changed\n')
            self.ChangeAnimation(f'{self.name}Hurt')
        elif type == 'true':
            damageTaken = damage
            self.health -= damage
            self.ChangeAnimation(f'{self.name}Hurt')
        elif type in self.weakness:
            print('Weak!')
            damageTaken = int(1.5* damage)
            self.health -= damageTaken
            self.ChangeAnimation(f'{self.name}Hurt')
        match type:
            case 'Rice':
                color = (238,217,196)
            case 'Fire':
                color = (255,116,0)
            case 'Water':
                color = (61,133,198)
            case 'true':
                color = (255,255,255)

        self.addEffect(f'{damageTaken}',(WIDTH / 1.5, HEIGHT / 6),color)
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
            target.addEffect(f'{self.name} used {chosenAttack[1]}!', (WIDTH / 3, HEIGHT / 6), duration=100)
            if chosenType == 'normal':
                chosenAttack[0](target)
            elif chosenType == 'dot': #Code looks dumb now, might change later
                chosenAttack[0](target)


    def applyStatEff(self):
        for i in self.statusEffects:
            i.apply(self)
            if self.health <= 0:
                self.isDead = True
            if i.duration <= 0:
                for j in self.statusList:
                    if j[0] == i.name:
                        self.statusList.remove(j)
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

    def ChangeAnimation(self,name):
        self.currAni = self.animationList[name]
            

    def render(self,dt):
        self.currAni.update(dt)

    def updateEffects(self, dt):
        # print(self.effectList)
        for index, effect in enumerate(self.effectList[:]): 
            effect['position'][1] -= 2

            effect['position'][0] -= index * rd.uniform(0.5, 1.5) 

            effect['timer'] -= 1
            print(effect['timer'])

            if effect['timer'] <= 0:
                print(self.effectList)
                print('EffectListRemoved')
                self.effectList.remove(effect)

    def addEffect(self, text, position,color= (153,153,153), duration=100):
            self.effectList.append({
                'text': text,
                'position': list(position), 
                'timer': duration,
                'color': color
            })

    