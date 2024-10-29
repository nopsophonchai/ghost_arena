import pygame


class Enemy:
    def __init__(self):
        self.damage = 1
        self.health = 10
        self.armor = 0


    def damage(self,damage):
        self.health -= (damage - self.armor)

