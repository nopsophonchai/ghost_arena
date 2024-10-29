import pygame
from src.Items.Card import Card
from src.Items.effects import gameEffects
from src.Items.Item import Item
from src.Items.Weapon import Weapon


class Player:
    def __init__(self):
        self.damage = 3
        self.health = 10
        self.armor = 0
        self.items = [Weapon('sword',self.damage)]
        self.deck = []
        self.deck.extend([Card('sword',Weapon('sword',self.damage))]*6)
        self.current = []


    def damageEnemy(self,damage):
        self.health -= (damage - self.armor)

    def drawCard(self):
        self.current.append(self.deck.pop())
    
    def addCard(self,card):
        self.deck.insert(card)
    

