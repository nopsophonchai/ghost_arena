from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *
from src.resources import *
from src.Player import Player
from src.Enemies.GongGoi import GongGoi
pygame.font.init()
import random as rd
gameFont = {
        'small': pygame.font.Font('./fonts/font.ttf', 24),
        'medium': pygame.font.Font('./fonts/font.ttf', 48),
        'large': pygame.font.Font('./fonts/font.ttf', 96)
}
class EnemySelection(BaseState):
    def __init__(self):
        super(Play, self).__init__()
        #start = 1,       ranking = 2
        self.option = 1
        self.round = 0



    def Exit(self):
        pass

    def Enter(self, params):
        self.round += 1
        enemiesGenerated = rd.randint(self.round+3,self.round+5)
        pass


    def update(self, dt, events):
        pass

    def render(self, screen):
        pass