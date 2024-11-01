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
        # self.enemy = GongGoi('Gong Goi',10,3)
        self.enemy = Preta('Preta',10,3)

        self.drawCount = 0
        self.turnCount = 0


    def Exit(self):
        pass

    def Enter(self, params):
        for i in range(3):
            self.player.drawCard()
        pass


    def update(self, dt, events):
        if self.turn == 0:
            if self.turnCount < 1:
                if len(self.player.statusEffects) != 0:
                    self.player.applyStatEff()
                elif len(self.player.buffs) != 0:
                    self.player.applyDebuffs()
                self.turnCount = 1
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.select = (self.select - 1) % (len(self.player.current) + 2)
                        print(self.select)
                    if event.key == pygame.K_RIGHT:
                        self.select = (self.select + 1) % (len(self.player.current) + 2)
                        print(self.select)
                    if event.key == pygame.K_RETURN:
                        self.confirm = True

            if self.confirm:
                self.confirm = False
                if self.select == 0 and self.drawCount == 0:
                    self.player.drawCard()
                    self.drawCount = 1
                elif self.drawCount == 1 and self.select == 0:
                    pass
                elif self.select == (len(self.player.current) + 1):
                    self.turn = 1
                else:
                    if self.player.current[self.select-1].item.weaponType == 'melee' and self.player.noMelee:
                        pass
                    else:
                        self.player.current[self.select-1].use(self.enemy)
                        self.player.useCard(self.player.current[self.select-1])
                        self.turn = 1   
                        self.turnCount = 0
                        self.drawCount = 0
                        if len(self.player.current)==0:
                            self.select = 0
                        print("-------Enemy's Turn-------")
        else:
            if len(self.enemy.statusEffects) != 0 and self.turnCount < 1:
                self.enemy.applyStatEff()
                self.turnCount = 1
            self.turnTimer += 1
            if self.turnTimer > 50:
                self.enemy.attack(self.player)
                self.turn = 0
                self.turnCount = 0
                self.turnTimer = 0
                print("-------Player's Turn-------")
                

    def render(self, screen):
        t_title = gameFont['small'].render(f"Enemy Health {self.enemy.health}", False, (255, 10, 40))
        rect = t_title.get_rect(center=(WIDTH / 1.5, HEIGHT / 3.75))
        screen.blit(t_title, rect)
        t_title = gameFont['small'].render(f"Player Health {self.player.health}", False, (255, 255, 255))
        rect = t_title.get_rect(center=(WIDTH / 3, HEIGHT / 3.75))
        screen.blit(t_title, rect)


        if self.turn == 0:
            for i in range(0, len(self.player.current)):
                if i+1 == self.select:
                    if self.player.current[i].item.weaponType == 'melee' and self.player.noMelee:
                        t_title = gameFont['small'].render(f"{self.player.current[i].name}", False, (80, 80, 80))
                        rect = t_title.get_rect(center=(WIDTH / 3.25+200*i, HEIGHT / 1.125))
                        screen.blit(t_title, rect)
                    else:
                        t_title = gameFont['small'].render(f"{self.player.current[i].name}", False, (0, 123, 255))
                        rect = t_title.get_rect(center=(WIDTH / 3.25+200*i, HEIGHT / 1.25))
                        screen.blit(t_title, rect)
                else:
                    t_title = gameFont['small'].render(f"{self.player.current[i].name}", False, (255, 255, 255))
                    rect = t_title.get_rect(center=(WIDTH / 3.25+200*i, HEIGHT / 1.125))
                    screen.blit(t_title, rect)
            if self.select == 0:
                t_title = gameFont['small'].render("Draw Card", False, (0, 123, 56))
                rect = t_title.get_rect(center=(WIDTH / 3.25 - 200, HEIGHT / 1.25))
                screen.blit(t_title, rect)
            else:
                t_title = gameFont['small'].render("Draw Card", False, (30, 255, 30))
                rect = t_title.get_rect(center=(WIDTH / 3.25 - 200, HEIGHT / 1.125))
                screen.blit(t_title, rect)
            if self.select == (len(self.player.current) + 1):
                t_title = gameFont['small'].render("End Turn", False, (180, 0, 0))
                rect = t_title.get_rect(center=(WIDTH / 3.25 + 200*(len(self.player.current)), HEIGHT / 1.25))
                screen.blit(t_title, rect)
            else:
                t_title = gameFont['small'].render("End Turn", False, (180, 0, 0))
                rect = t_title.get_rect(center=(WIDTH / 3.25 + 200*(len(self.player.current)), HEIGHT / 1.125))
                screen.blit(t_title, rect)