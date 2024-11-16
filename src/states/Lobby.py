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

class Lobby(BaseState):
    def __init__(self):
        super(Lobby, self).__init__()
        self.option = 0 
        self.round = 0
        self.confirm = False
        self.select = 0
        self.enemiesList = []
        self.roundEnd = True
        self.player = Player()

        self.background_image = pygame.transform.scale(pygame.image.load("./graphics/shopBG1.png"), (WIDTH, HEIGHT))

    def Reset(self):
        self.option = 0
        self.round = 0
        self.confirm = False
        self.select = 0
        self.enemiesList = []
        self.roundEnd = True
        self.player = Player()
        

    def Exit(self):
        pass

    def Enter(self, params):
        if 'player' in params:
            self.player = params['player']
            self.player.refresh()
            
        if 'round' in params:
            self.round = params['round']
        self.player.ChangeAnimation('playerIdle')
    def update(self, dt, events):
       self.player.render(dt)
       for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.option = (self.option - 1) % 3  # Cycle options left
                elif event.key == pygame.K_RIGHT:
                    self.option = (self.option + 1) % 3  # Cycle options right
                elif event.key == pygame.K_RETURN:
                    # Navigate based on selected option
                    if self.option == 0:
                        stateManager.Change('character', {'player': self.player, 'round': self.round})
                    elif self.option == 1:
                        stateManager.Change('shop', {'player': self.player, 'round': self.round})
                    elif self.option == 2:
                        stateManager.Change('select', {'player': self.player, 'round': self.round})

    def render(self, screen):
        screen.blit(self.player.currAni.image,(WIDTH//2 - 64,HEIGHT//2 - 64,0,0))
        # screen.blit(pygame.image.load('graphics/swordCard.png'),(WIDTH//2-60,HEIGHT//1.5,0,0))

        self.player.items['sword'].render(screen,WIDTH//4,HEIGHT//1.5)
        self.player.items['Fire'].render(screen,WIDTH//1.5,HEIGHT//3)




        

