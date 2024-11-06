import pygame
import math


class Card:
    def __init__(self,name,item):
        self.name = name
        self.item = item #This is class Item
    def use(self,target):
        self.item.attack(target)
        print('called')
    