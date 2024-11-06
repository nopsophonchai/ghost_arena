from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *
from src.resources import *
from src.Player import Player
from src.Enemies.GongGoi import GongGoi
from src.Enemies.Preta import Preta
pygame.font.init()
import random as rd
gameFont = {
        'small': pygame.font.Font('./fonts/font.ttf', 24),
        'medium': pygame.font.Font('./fonts/font.ttf', 48),
        'large': pygame.font.Font('./fonts/font.ttf', 96)
}
class Character(BaseState):
    def __init__(self):
        super(Character, self).__init__()
        #start = 1,       ranking = 2
        self.option = 1
        self.round = 0
        self.confirm = False
        self.select = 0

        self.enemiesList = []
        self.roundEnd = True
        self.player = Player()
        self.page = 1

    def Exit(self):
        pass

    def Enter(self, params):
        if 'player' in params:
            self.player = params['player']

    def update(self, dt, events):
       for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    stateManager.Change('lobby',{'player': self.player})
                if event.key == pygame.K_UP:
                    self.page += 1
    def render(self, screen):
        text_surface = gameFont['small'].render(f'Player Health: {self.player.health}', True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(text_surface, rect)
        text_surface = gameFont['small'].render(f'Player Damage: {self.player.damage}', True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2.5))
        screen.blit(text_surface, rect)
        text_surface = gameFont['small'].render(f"Player Items: {self.player.items['sword'].name}", True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text_surface, rect)