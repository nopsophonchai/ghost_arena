import pygame
from src.Items.Card import Card
from src.Items.effects import gameEffects
from src.Items.Item import Item
from src.Items.Weapon import Weapon
import random as rd


class Player:
    def __init__(self):
        self.damage = 3
        self.health = 10
        self.maxHealth = 10
        self.armor = 0
        self.items = {'sword':Weapon('Sword',self.damage,'melee'),'bow':Weapon('Bow',int(self.damage//1.5),'range')}
        self.deck = []
        self.deck.extend([Card('sword',self.items['sword'])]*6 + [Card('bow',self.items['bow'])]*6)
        rd.shuffle(self.deck)
        self.deckCopy = self.deck[:]
        self.current = []

        self.statusEffects = []
        self.buffs = []
        self.noMelee = False
        self.noArmor = False

        self.gold = 10

    def damageEnemy(self,damage):
        if not self.noArmor:
            self.health -= (damage - self.armor)
        else:
            self.health -= (damage)

        print(f'Player Damage Taken: {damage}')
    def drawCard(self):
        print(f'Deck when drawn: {self.deck}')
        self.current.append(self.deck.pop())
    
    def addCard(self,card):
        self.deck.insert(0,card)
        print(f'Deck when added: {self.deck}')

    def playerScale(self,damage):
        for i in self.items.values():
            i.damage += damage
    
    def addItem(self,item):
        self.items[f'{item.name}'] = item

    def useCard(self,card):
        self.current.remove(card)
        self.addCard(card)
        print(f'Deck when used: {self.deck}')

    def refresh(self):
        self.deck.extend(self.current)
        self.current = []
        self.health = self.maxHealth
    
    def applyStatEff(self):
        print('Poison!')
        for i in self.statusEffects:
            i.apply(self)
            if i.duration <= 0:
                self.statusEffects.remove(i)
    def applyDebuffs(self):
        print(self.noMelee)
        for debuff in self.buffs[:]: 
            debuff.apply(self)
            if debuff.duration <= 0:
                debuff.remove(self)  
                self.buffs.remove(debuff)

    

