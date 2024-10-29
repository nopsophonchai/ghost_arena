from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *
from src.resources import *
from src.Player import Player
pygame.font.init()
import random as rd
gameFont = {
        'small': pygame.font.Font('./fonts/font.ttf', 24),
        'medium': pygame.font.Font('./fonts/font.ttf', 48),
        'large': pygame.font.Font('./fonts/font.ttf', 96)
}
class Play(BaseState):
    def __init__(self):
        super(Play, self).__init__()
        #start = 1,       ranking = 2
        self.option = 1
        self.showNum = False
        self.playerHealth = 10
        self.enemyHealth = 10
        self.select = 0
        self.enemySelect = 0
        self.currentTurn = 1
        self.turn = 0
        self.confirm = False
        self.turnTimer = 0

        self.player = Player()
        self.enemy = Player()



    def Exit(self):
        pass

    def Enter(self, params):
        for i in range(3):
            self.player.drawCard()
        pass


    def update(self, dt, events):
        if self.turn == 0:
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.select = (self.select - 1) % len(self.player.current)
                    if event.key == pygame.K_RIGHT:
                        self.select = (self.select + 1) % len(self.player.current)
                    if event.key == pygame.K_RETURN:
                        self.confirm = True

            if self.confirm:
                self.confirm = False
                self.player.current[self.select].use(self.enemy)
                self.turn = 1   
        else:
            self.turnTimer += 1
            if self.turnTimer > 50:
                self.enemySelect = rd.randint(0,1)
                match self.enemySelect:
                    case 0:
                        self.player.damageEnemy(1)
                    case 1:
                        self.enemy.health += 1
                self.turn = 0
                self.turnTimer = 0

                

    def render(self, screen):
        t_title = gameFont['small'].render(f"Enemy Health {self.enemy.health}", False, (255, 10, 40))
        rect = t_title.get_rect(center=(WIDTH / 1.5, HEIGHT / 3.75))
        screen.blit(t_title, rect)
        t_title = gameFont['small'].render(f"Player Health {self.player.health}", False, (255, 255, 255))
        rect = t_title.get_rect(center=(WIDTH / 3, HEIGHT / 3.75))
        screen.blit(t_title, rect)


        if self.turn == 0:
            for i in range(len(self.player.current)):
                if i == self.select:
                    t_title = gameFont['small'].render(f"{self.player.current[i].name}", False, (0, 123, 255))
                    rect = t_title.get_rect(center=(WIDTH / 3.25+200*i, HEIGHT / 1.25))
                    screen.blit(t_title, rect)
                else:
                    t_title = gameFont['small'].render(f"{self.player.current[i].name}", False, (255, 255, 255))
                    rect = t_title.get_rect(center=(WIDTH / 3.25+200*i, HEIGHT / 1.125))
                    screen.blit(t_title, rect)
               