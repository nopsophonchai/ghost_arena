import pygame
from src.Items.Card import Card
from src.Items.effects import gameEffects, playerEffects
from src.Items.Item import Item
from src.Items.Weapon import Weapon
from src.Items.Rice import Rice
from src.Items.Fire import Fire
from src.Items.Water import Water
import random as rd
from src.resources import aniList
from src.constants import *
import math

class Player:
    def __init__(self):
        self.damage = 3
        self.health = 10
        self.maxHealth = 10
        self.maxDamage = 3
        self.armor = 0
        self.items = {'sword':Weapon('Sword',self.damage,'melee',[],[]),'bow':Weapon('Bow',int(self.damage//1.5),'range')}
        # self.items = {'fire':Fire('Fire',self.damage,'Fire')}
        # self.items = {'rice':Rice('rice',self.damage,'Rice')}
        # self.items = {'water':Water('water',self.damage,'Water')}
        self.deck = []
        
        self.deck.extend([Card('sword',self.items['sword'])]*6 + [Card('bow',self.items['bow'])]*6 )
        # self.deck.extend([Card('fire',self.items['fire'])]*6)
        # self.deck.extend([Card('rice',self.items['rice'])]*6)
        # self.deck.extend([Card('water',self.items['water'])]*6)
        
        rd.shuffle(self.deck)
        self.deckCopy = self.deck[:]
        self.current = []

        self.statusEffects = []
        self.buffs = []
        self.noMelee = False
        self.noArmor = False
        
        self.noCard = False

        self.gold = 10


        self.animationList = aniList
        self.currAni = None

        self.effectList = []
        self.statusList = []

    def damageEnemy(self,damage,type='normal'):
        damageTaken = 0
        color = (153,153,153)
        if not self.noArmor:
            damageTaken = (damage - self.armor)
            self.health -= damageTaken
        else:
            damateTaken = damage
            self.health -= (damage)

        # print(f'Player Damage Taken: {damage}')
        self.addEffect(f'{damageTaken}',(WIDTH / 3.5, HEIGHT / 6), color,duration=100)
    def drawCard(self):
        # print(f'Deck when drawn: {self.deck}')
        self.current.append(self.deck.pop())
    
    def addCard(self,card):
        self.deck.insert(0,card)
        # print(f'Deck when added: {self.deck}')

    def playerScale(self,damage):
        for i in self.items.values():
            i.damage += damage
        
        self.items['bow'].damage = self.maxDamage
        self.items['bow'].damage = math.ceil(self.items['bow'].damage / 1.5)

    def useCard(self,card):
        self.current.remove(card)
        self.addCard(card)
        # print(f'Deck when used: {self.deck}')

    def refresh(self):
        for i in self.items.values():
            i.useThree = 0
        self.deck.extend(self.current)
        self.current = []
        self.damage = self.maxDamage
        # self.health = self.maxHealth

    def addItem(self,item):
        self.items[f'{item.name}'] = item
        card = Card(item.name,item)
        self.deck.extend([card]*6)
        rd.shuffle(self.deck)
    
    def applyStatEff(self):
        # print('Poison!')
        for i in self.statusEffects:
            i.apply(self)
            self.addEffect(f'{i.name}', (WIDTH / 3, HEIGHT / 6), duration=100)
            if i.duration <= 0:
                for j in self.statusList:
                    if i.name == j[0]:
                        self.statusList.remove(j)
                self.statusEffects.remove(i)
                
    def applyDebuffs(self):
        print(f'No card: {self.noCard}')
        for debuff in self.buffs[:]: 
            debuff.apply(self)
            if debuff.duration <= 0:
                debuff.remove(self)  
                for j in self.statusList:
                    if debuff.name == j[0]:
                        self.statusList.remove(j)
                self.buffs.remove(debuff)

    def ChangeAnimation(self,name):
        self.currAni = self.animationList[name]
        # print(self.currAni.images)
        print('called')

    def render(self,dt):
        self.currAni.update(dt)
    
    def updateEffects(self, dt):
        for index, effect in enumerate(self.effectList[:]): 
            effect['position'][1] -= 2

            effect['position'][1] -= index * 2 

            effect['timer'] -= 1

            if effect['timer'] <= 0:
                self.effectList.remove(effect)

    def addEffect(self, text, position, color = (153,153,153),duration=100):
            self.effectList.append({
                'text': text,
                'position': list(position), 
                'timer': duration,
                'color':color
            })

    
