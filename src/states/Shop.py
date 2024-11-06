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
        self.willlastmeallmylifewoahyessoshouldweeeeeeeeheheimspendingallllllllyeahthistimeeeeeeeeeeeeeeeoh = 0


    def Exit(self):
        pass

    def Enter(self, params):
        if 'player' in params:
            self.player = params['player']
        
        self.itemList = list(gameEffects.values())
        self.chosenList = rd.sample(self.itemList,4)
    def update(self, dt, events):
       for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.select = (self.select - 1) % (7)
                    print(self.select)
                if event.key == pygame.K_RIGHT:
                    self.select = (self.select + 1) % (7)
                    print(self.select)
                if event.key == pygame.K_RETURN:
                    self.confirm = True
    def render(self, screen):
        locations = [(WIDTH / 3, HEIGHT / 3),(WIDTH / 1.5, HEIGHT / 3),(WIDTH / 3, HEIGHT / 1.5), (WIDTH / 1.5, HEIGHT / 1.5), (WIDTH / 3, HEIGHT / 1.25),(WIDTH / 1.5, HEIGHT / 1.25)]
        item_spacing = 200
        total_width = item_spacing * (4)
        start_x = (WIDTH - total_width + 200) / 2
        text_surface = gameFont['small'].render(f'Back to fighting!', True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        if self.select == 6:
            pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
        screen.blit(text_surface, rect)
        for i in range(4):
            text_surface = gameFont['small'].render(self.chosenList[i][1], True, (255, 255, 255))
            rect = text_surface.get_rect(center=locations[i])
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