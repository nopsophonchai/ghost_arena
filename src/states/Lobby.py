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
        #start = 1,       ranking = 2
        self.option = 1
        self.round = 0
        self.confirm = False
        self.select = 0

        self.enemiesList = []
        self.roundEnd = True
        self.player = Player()

        self.bg_image = pygame.image.load("./graphics/bg_lobby.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.smoke = pygame.image.load("./graphics/smoke.png")
        self.a_left = pygame.image.load("./graphics/arrow_left.png")
        self.a_right = pygame.image.load("./graphics/arrow_right.png")

    def Reset(self):
        self.option = 1
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
                    stateManager.Change('character',{'player': self.player,'round':self.round})
                if event.key == pygame.K_RIGHT:
                    stateManager.Change('shop',{'player': self.player,'round':self.round})
                if event.key == pygame.K_RETURN:
                    stateManager.Change('select',{'player': self.player,'round':self.round})
    def render(self, screen):
        new_wright = self.a_right.get_width() // 3
        new_hright = self.a_right.get_height() // 3
        scaled_rightimage = pygame.transform.scale(self.a_right, (new_wright, new_hright))
        new_wleft = self.a_left.get_width() // 3
        new_hleft = self.a_left.get_height() // 3
        scaled_leftimage = pygame.transform.scale(self.a_left, (new_wleft, new_hleft))
        screen.blit(self.bg_image, (0, 0))
        screen.blit(self.smoke,(WIDTH//2 - 64,HEIGHT//2 - 250,0,0))
        screen.blit(self.player.currAni.image,(WIDTH//2 - 64,HEIGHT//2 - 64,0,0))
        screen.blit(scaled_rightimage, (WIDTH // 1.5+220, HEIGHT // 4 + 415))
        #screen.blit(scaled_leftimage, (0,HEIGHT -115))
        screen.blit(scaled_leftimage, (0,0))
        # screen.blit(pygame.image.load('graphics/swordCard.png'),(WIDTH//2-60,HEIGHT//1.5,0,0))

        # self.player.items['sword'].render(screen,WIDTH//4-100,HEIGHT//1.5 -100)
        # self.player.items['Fire'].render(screen,WIDTH//1.5,HEIGHT//4)
       

      




        

