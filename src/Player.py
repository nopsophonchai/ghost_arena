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
        self.armor = 0
        self.items = {'sword':Weapon('sword',self.damage,'melee',[gameEffects['theSun'][0],gameEffects['niceguy'][0]]),'bow':Weapon('bow',int(self.damage//1.5),'range')}
        self.deck = []
        self.deck.extend([Card('sword',self.items['sword'])]*6 + [Card('bow',self.items['bow'])]*6)
        rd.shuffle(self.deck)
        self.current = []

        self.statusEffects = []
        self.buffs = []
        self.noMelee = False
        self.noArmor = False

        self.gold = 0

    def damageEnemy(self,damage):
        if not self.noArmor:
            self.health -= (damage - self.armor)
        else:
            self.health -= (damage)

        print(f'Player Damage Taken: {damage}')
    def drawCard(self):
        self.current.append(self.deck.pop())
    
    def addCard(self,card):
        self.deck.insert(0,card)
    
    def addItem(self,item):
        self.items[f'{item.name}'] = item

    def useCard(self,card):
        self.current.remove(card)
        self.addCard(card)

    def refresh(self):
        self.current = []
        self.deck = []
        self.deck.extend([Card('sword',self.items['sword'])]*6 + [Card('bow',self.items['bow'])]*6)
        rd.shuffle(self.deck)
    
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

    

