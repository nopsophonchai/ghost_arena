import pygame
import math


class Card:
    def __init__(self,name,item):
        self.name = name
        self.item = item #This is class Item
    def use(self,target,player):
        self.item.attack(target)
        print('called')

    def heal(self,player,amount):
        player.health = min(player.maxHealth, player.health + amount)
    
    def render(self,screen,x,y):
        screen.blit(pygame.image.load(f'graphics/cards.png/{self.name}.png'),(x,y,0,0))
    
