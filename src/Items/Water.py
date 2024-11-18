import traceback
from src.Items.Item import Item
from src.Items.StatusEffect import StatusEffect
import math
import pygame
from src.constants import *
from src.resources import *

class Water(Item):
    def __init__(self,name, damage,spellType):
        super().__init__(name)
        self.damage = damage
        self.type = 'Spell'
        self.weaponType = 'range'
        self.damageType = 'Water'
        self.interfaceFlag = False
        self.spellList = [('Splash',self.splash,f'Deals {self.damage} water damage'),('Water of Life',self.waterOfLife,f'Heal for {math.ceil(self.damage*1.5)} health'),('Tsunami',self.tsunami,f'Makes enemy health\nequals to yours\nalong with dealing\n{self.damage} water damage')]
        self.effects = []
        self.playerEffects = []


    def attack(self,target,player,selected):
        self.interfaceFlag = True
        chosenSpell = self.spellList[selected][1]
        chosenSpell(target,player)

    def splash(self,target,player):
        if target:
            target.damageEnemy(self.damage,self.damageType)
            player.addEffect(f'{self.damage}',(WIDTH / 1.5, HEIGHT / 6), (61,133,198),duration=100)
            target.damage -= 1
            player.addEffect(f'Damage reduced by 1!',(WIDTH / 1.5, HEIGHT / 6))
    
    def waterOfLife(self,target,player):
        if player:
            player.health += math.ceil(self.damage*1.5)
            player.addEffect(f'+{math.ceil(self.damage*1.5)}',(WIDTH / 3.5, HEIGHT / 6), (143,206,0),duration=100)
    
    def tsunami(self,target,player):
        if self.useThree < 1:
            if target:
                target.health = player.health 
                target.damageEnemy(self.damage)
                self.useThree += 1
                player.addEffect(f'ENEMY HEALTH = {player.health}!',(WIDTH / 1.5, HEIGHT / 6), (61,133,198),duration=100)
                player.addEffect(f'{self.damage}',(WIDTH / 1.5, HEIGHT / 6), (61,133,198),duration=100)
                print('TSUNAMI')
        else:
            player.addEffect(f'Max number of casts met, damaging for 1!',(WIDTH / 1.5, HEIGHT / 6), (61,133,198),duration=100)
            target.damageEnemy(1)

    def getCombinedEffects(self):
        return self.effects + self.playerEffects
    
    def render(self,screen,x,y):
        cardX = x
        cardY = y
        screen.blit(pygame.image.load(f'graphics/items.png/{self.name}.png'),(cardX,cardY,0,0))

        text_surface = gameFont['small'].render(f"Water", True, (0, 0, 0))
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
