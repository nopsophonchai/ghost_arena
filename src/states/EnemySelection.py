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
class EnemySelection(BaseState):
    def __init__(self):
        super(EnemySelection, self).__init__()
        #start = 1,       ranking = 2
        self.option = 1
        self.round = 0
        self.confirm = False
        self.select = 0

        self.enemiesList = []
        self.roundEnd = True
        self.player = None


    def Exit(self):
        self.select = 0

    def Enter(self, params):
        self.player = params['player']
        print(f'Player Select Health: {self.player.health}')
        if self.roundEnd == True:
            self.round += 1
            enemiesGenerated = rd.randint(min(self.round+3,6),6)
            # enemiesGenerated = 1
            allEnemies = ['Preta','GongGoi']
            for enemy in range(enemiesGenerated):
                selectedEnemy = rd.choice(allEnemies)
                addedEnemy = None
                match selectedEnemy:
                    case 'Preta': addedEnemy = Preta('Preta',(10+(2*(self.round-1))),(3+(self.round-1)))
                    case 'GongGoi': addedEnemy = GongGoi('GongGoi',(4+(2*(self.round-1))),(2+(self.round-1)))
                self.enemiesList.append(addedEnemy)
            # print(self.enemiesList)
            self.roundEnd = False
        else:
            for i in self.enemiesList:
                if i.isDead:
                    self.enemiesList.remove(i)
                    print(f'Removed {i}')
            # print(len(self.enemiesList))
            if len(self.enemiesList) == 0:
                self.roundEnd = True
                stateManager.Change('lobby',{'player':self.player})


    def update(self, dt, events):

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.select = (self.select - 1) % (len(self.enemiesList))
                    print(self.select)
                if event.key == pygame.K_RIGHT:
                    self.select = (self.select + 1) % (len(self.enemiesList))
                    print(self.select)
                if event.key == pygame.K_RETURN:
                    self.confirm = True
        if self.confirm:
            payload = {'enemy':self.enemiesList[self.select],'round':self.round,'player':self.player}
            stateManager.Change('play',payload)
            self.confirm = False

    def render(self, screen):
        item_spacing = 200
        total_width = item_spacing * (len(self.enemiesList) - 1)
        start_x = (WIDTH - total_width) / 2
        text_surface = gameFont['small'].render(f'Round {self.round}', True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(text_surface, rect)
        for i in range(len(self.enemiesList)):
            text_surface = gameFont['small'].render(self.enemiesList[i].name, True, (255, 255, 255))
            rect = text_surface.get_rect(center=(start_x + item_spacing * i, HEIGHT / 1.25))
            if self.select == i:
                pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
            screen.blit(text_surface, rect)