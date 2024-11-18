import traceback
from src.Items.Item import Item
from src.Items.StatusEffect import StatusEffect
import random as rd
import pygame
from src.resources import *
from src.constants import *

class Rice(Item):
    def __init__(self,name, damage,spellType):
        super().__init__(name)
        self.damage = damage
        self.type = 'Spell'
        self.weaponType = 'range'
        self.damageType = 'Rice'
        self.interfaceFlag = False
        self.spellList = [('Throw',self.throw,f'Deal {self.damage} rice damage'),('Eat',self.eat,f'Heal for {self.damage // 2} health'),('Bin Tha Bat',self.binthabat,f'5% chance to \ninstantly kill enemy')]
        self.effects = []
        self.playerEffects = []


    def attack(self,target,player,selected):
        self.interfaceFlag = True
        chosenSpell = self.spellList[selected][1]
        chosenSpell(target,player)

    def throw(self,target,player):
        if target:
            target.damageEnemy(self.damage,self.damageType)
            player.addEffect(f'{self.damage}',(WIDTH / 1.5, HEIGHT / 6), (238,217,196),duration=100)

    
    def eat(self,target,player):
        if player:
            player.health += self.damage // 2
            player.addEffect(f'+{self.damage // 2}',(WIDTH / 3.5, HEIGHT / 6), (143,206,0),duration=100)

    def binthabat(self,target,player):
        if target:
            prob = rd.random()
            if prob <= 0.05:
                target.damageEnemy(1000000,self.damageType)
                player.addEffect(f'{self.damage}',(WIDTH / 1.5, HEIGHT / 6), (238,217,196),duration=100)
            else:
                player.addEffect(f'Bad Luck!',(WIDTH / 1.5, HEIGHT / 6), (238,217,196),duration=100)

    def getCombinedEffects(self):
        return self.effects + self.playerEffects
    
    def render(self,screen,x,y):
        cardX = x
        cardY = y
        screen.blit(pygame.image.load(f'graphics/items.png/{self.name}.png'),(cardX,cardY,0,0))

        text_surface = gameFont['small'].render(f"Rice", True, (0, 0, 0))
        rect = text_surface.get_rect(center=(cardX + 90, cardY + 22))
        screen.blit(text_surface, rect)

        text_surface = pygame.font.Font('./fonts/font.ttf', 16).render(f"Damage:", True, (0, 0, 0))
        rect = text_surface.get_rect(center=(cardX + 260, cardY + 20))
        screen.blit(text_surface, rect)

        text_surface = pygame.font.Font('./fonts/font.ttf', 16).render(f"{self.damage}", True, (0, 0, 0))
        rect = text_surface.get_rect(center=(cardX + 260, cardY + 40))
        screen.blit(text_surface, rect)

        if len(self.spellList) > 0:
            effect_y_position = 65
            effect_y_positionTwo = 10
            for i in range(3):
                text_surface = pygame.font.Font('./fonts/font.ttf', 12).render(f"{self.spellList[i][0]}", True, (0, 0, 0))
                rect = text_surface.get_rect(center=(cardX + 260, cardY + effect_y_position))
                screen.blit(text_surface, rect)
                effect_y_position += 10 
                effect_y_positionTwo = 0
                description_lines = self.spellList[i][2].split('\n')
                for line in description_lines:
                    text_surface = pygame.font.Font('./fonts/font.ttf', 12).render(line, True, (0, 0, 0))
                    rect = text_surface.get_rect(center=(cardX + 260, cardY + effect_y_position + effect_y_positionTwo))
                    screen.blit(text_surface, rect)
                    effect_y_positionTwo += 10 
                effect_y_position += 60 
