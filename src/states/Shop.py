from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *
from src.resources import *
from src.Player import Player
from src.Enemies.GongGoi import GongGoi
from src.Enemies.Preta import Preta
from src.Items.Weapon import Weapon
from src.Items.effects import gameEffects
pygame.font.init()
import random as rd
gameFont = {
        'small': pygame.font.Font('./fonts/font.ttf', 24),
        'medium': pygame.font.Font('./fonts/font.ttf', 48),
        'large': pygame.font.Font('./fonts/font.ttf', 96)
}
class Shop(BaseState):
    def __init__(self):
        super(Shop, self).__init__()
        self.confirm = False
        self.select = 0

        self.healthBought = 0
        self.damageBought = 0
        self.healthPrice = 2
        self.damagePrice = 2

        self.weaponSelect = False
        self.chosenEffect = None

    def Exit(self):
        pass

    def Enter(self, params):
        if 'player' in params:
            self.player = params['player']
        
        self.itemList = list(gameEffects.values())
        self.chosenList = rd.sample(self.itemList,4)
    def update(self, dt, events):
        # print(self.player.items['sword'].effects)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.weaponSelect:
                        self.select = (self.select - 1) % (len(list(self.player.items)))
                    else:
                        self.select = (self.select - 1) % (7)
                    # print(self.select)
                if event.key == pygame.K_RIGHT:
                    if self.weaponSelect:
                        self.select = (self.select + 1) % (len(list(self.player.items)))
                    else:
                        self.select = (self.select + 1) % (7)
                    # print(self.select)
                if event.key == pygame.K_RETURN:
                    self.confirm = True
        if self.confirm:
            self.confirm = False
            if self.weaponSelect:
                # print('\n')
                # print(self.chosenEffect)
                list(self.player.items.items())[self.select][1].effects.append(self.chosenEffect)
                self.weaponSelect = False
            if not self.weaponSelect:
                if self.select == 6:
                    stateManager.Change('lobby',{'player':self.player})
                if self.select == 4:
                    if self.player.gold - self.healthPrice >= 0:
                        self.player.maxHealth += 2

                        self.player.gold -= self.healthPrice
                        self.healthPrice = self.healthPrice + (2 * self.healthBought)
                        self.healthBought += 1
                if self.select == 5:
                    if self.player.gold - self.damagePrice >= 0:
                        self.player.damage += 1

                        self.player.gold -= self.damagePrice
                        self.damagePrice = self.damagePrice + (2 * self.damageBought)
                        self.player.playerScale(1)
                        self.damageBought += 1
                if self.select < 4:
                    if self.player.gold >= self.chosenList[self.select][2]:
                        self.weaponSelect = True
                        self.player.gold -= self.chosenList[self.select][2]
                        self.chosenEffect = (self.chosenList[self.select][0],self.chosenList[self.select][1])
                        # print(self.chosenEffect)


                    
    def render(self, screen):
        if not self.weaponSelect:
            locations = [(WIDTH / 3, HEIGHT / 3),(WIDTH / 1.5, HEIGHT / 3),(WIDTH / 3, HEIGHT / 1.5), (WIDTH / 1.5, HEIGHT / 1.5), (WIDTH / 3, HEIGHT / 1.25),(WIDTH / 1.5, HEIGHT / 1.25)]
            priceLocations = [(WIDTH / 3, HEIGHT / 2.7),(WIDTH / 1.5, HEIGHT / 2.7),(WIDTH / 3, HEIGHT / 1.4), (WIDTH / 1.5, HEIGHT / 1.4)]
            item_spacing = 200
            total_width = item_spacing * (4)
            start_x = (WIDTH - total_width + 200) / 2
            text_surface = gameFont['small'].render(f'Back to fighting!', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            if self.select == 6:
                pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
            screen.blit(text_surface, rect)
            for i in range(4):
                text_surface = gameFont['small'].render(f'{self.chosenList[i][1]}', True, (255, 255, 255))
                rect = text_surface.get_rect(center=locations[i])
                if self.select == i:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                screen.blit(text_surface, rect)
                text_surface = gameFont['small'].render(f'{self.chosenList[i][2]}', True, (255, 255, 255))
                rect = text_surface.get_rect(center=priceLocations[i])
                if self.select == i:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Increase health by 2', True, (255, 255, 255))
            rect = text_surface.get_rect(center=locations[4])
            if self.select == 4:
                pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Increase damage by 1', True, (255, 255, 255))
            rect = text_surface.get_rect(center=locations[5])
            if self.select == 5:
                pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
            screen.blit(text_surface, rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Gold: {self.player.gold}', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(325,95))
            screen.blit(text_surface,rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Damage: {self.player.damage}', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(325,120))
            screen.blit(text_surface,rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Health: {self.player.health}', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(325,150))
            screen.blit(text_surface,rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Health Price: {self.healthPrice}', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(600,150))
            screen.blit(text_surface,rect)

        if self.weaponSelect:
            item_spacing = 200
            total_width = item_spacing * (len(list(self.player.items)) - 1)
            start_x = (WIDTH - total_width) / 2
            text_surface = gameFont['small'].render(f'Which item do you want to enchant?', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3))
            screen.blit(text_surface, rect)
            for i in range(len(list(self.player.items))):
                text_surface = gameFont['small'].render(list(self.player.items.items())[i][1].name, True, (255, 255, 255))
                rect = text_surface.get_rect(center=(start_x + item_spacing * i, HEIGHT / 1.25))
                if self.select == i:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                screen.blit(text_surface, rect)


