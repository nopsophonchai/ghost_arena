from src.states.BaseState import BaseState
import pygame, sys
from src.Items.Debuff import Debuff
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
        self.interface = False
        # self.enemy = GongGoi('Gong Goi',10,3)
        self.enemy = Preta('Preta',10,3)

        self.drawCount = 0
        self.turnCount = 0
        self.buffCount = 0

        self.deadTimer = 0
        self.round = 0

        self.interfaceSelect = 0
        self.interfaceConfirm = False

    def Exit(self):
        self.player.refresh()


    def Enter(self, params):
        self.player = params['player']
        for i in range(3):
            self.player.drawCard()
        self.enemy = params['enemy']
        self.round = params['round']
        self.turn = 0
        print(self.player)



    def update(self, dt, events):
        if self.turn == 0:
            if not self.interface:
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
                self.confirmHandle(dt, events)
        else:
            if not self.enemy.isDead:
                if len(self.enemy.statusEffects) != 0 and self.turnCount < 1:
                    self.enemy.applyStatEff()
                    self.turnCount = 1
                if len(self.enemy.buffs) != 0 and self.buffCount < 1:
                    self.enemy.applyDebuffs()
                    self.buffCount = 1
                self.turnTimer += 1
                if self.turnTimer > 50:
                    self.enemy.attack(self.player)
                    self.turn = 0
                    self.turnCount = 0
                    self.buffCount = 0
                    self.turnTimer = 0
                    print("-------Player's Turn-------")

    def confirmHandle(self,dt, events):
        if not self.interface:
            self.confirm = False
            if self.select == 0 and self.drawCount == 0:
                self.player.drawCard()
                self.drawCount = 1
            elif self.drawCount == 1 and self.select == 0:
                pass
            elif self.select == (len(self.player.current) + 1):
                self.turn = 1
                self.drawCount = 0
                self.turnCount = 0
            else:
                print(self.player.noMelee)
                if self.player.current[self.select-1].item.weaponType == 'melee' and self.player.noMelee:
                    pass
                else:
                    chosenCard = self.player.current[self.select-1]
                    if chosenCard.item.type == 'Weapon':
                        if chosenCard.item.bungieGum == True:
                            self.interface = True
                            self.confirm = True
                        else:
                            chosenCard.use(self.enemy,self.player)
                            self.player.useCard(self.player.current[self.select-1])
                            self.turn = 1   
                            self.turnCount = 0
                            self.drawCount = 0
                            if len(self.player.current)==0:
                                self.select = 0
                            print("-------Enemy's Turn-------")
                    if self.enemy.health <= 0:
                        self.enemy.isDead = True
                        self.deadTimer = 120
                        # print(self.enemy.health)
                        self.player.health = min(self.player.maxHealth,self.player.health + (self.enemy.maxHealth // 2))
                        print(self.player.health)
                        self.player.gold += self.enemy.gold + (self.round*2)

                        
                    
        else:
            print("Welcome to the show")
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.interfaceSelect = (self.interfaceSelect - 1) % (3)
                    if event.key == pygame.K_DOWN:
                        self.interfaceSelect = (self.interfaceSelect + 1) % (3)
                    if event.key == pygame.K_RETURN:
                        self.interfaceConfirm = True
            
            if self.interfaceConfirm:
                chosenCard = self.player.current[self.select-1]
                match self.interfaceSelect:  
                    case 0: chosenCard.use(self.enemy,self.player)
                    case 1: chosenCard.heal(self.player,int(chosenCard.item.damage // 2))
                    case 2: 
                        def apply(target):
                            target.miss = True
                            print(f'Changed Miss: {target.miss}')
                        def remove(target):
                            target.miss = False
                        sun = Debuff('sun',apply,remove,2)
                        self.enemy.buffs.append(sun)
                self.player.useCard(self.player.current[self.select-1])
                self.interface = False
                self.interfaceConfirm = False
                self.confirm = False
                self.turn = 1   
                self.turnCount = 0
                self.drawCount = 0
                if len(self.player.current)==0:
                    self.select = 0
                print("-------Enemy's Turn-------")
                if self.enemy.health <= 0:
                    self.enemy.isDead = True
                    self.deadTimer = 120
                    # print(self.enemy.health)
                    self.player.health = min(self.player.maxHealth,self.player.health + (self.enemy.maxHealth // 2))
                    print(self.player.health)
                    self.player.gold += self.enemy.gold + (self.round*2)
                

    def render(self, screen):
        
        if self.deadTimer > 0:
            message_surface = gameFont['small'].render(f'You have defeated {self.enemy.name}!', True, (255, 215, 0))
            message_rect = message_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surface, message_rect)
            message_surface = gameFont['small'].render(f'Gold earned {self.enemy.gold+(2*self.round)}!', True, (255, 215, 0))
            message_rect = message_surface.get_rect(center=(WIDTH / 2, HEIGHT / 1.5))
            screen.blit(message_surface, message_rect)
            message_surface = gameFont['small'].render(f'Health recovered {self.enemy.maxHealth // 2}!', True, (255, 215, 0))
            message_rect = message_surface.get_rect(center=(WIDTH / 2, HEIGHT / 1.25))
            screen.blit(message_surface, message_rect)
            self.deadTimer -= 1
            if self.deadTimer <= 0:
                stateManager.Change('select',{'player':self.player})
        else:
            t_title = gameFont['small'].render(f"{self.enemy.name}: {self.enemy.health}", False, (255, 10, 40))
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
        if self.interface:
            pygame.draw.rect(screen, (255, 255, 255), (WIDTH/2 - 150, HEIGHT/2 - 150, 300, 300))
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH/2 - 145, HEIGHT/2 - 145, 290, 290))
            titles = ["Attack", "Heal", "Block"]
            line_height = 50 
            box_center_y = HEIGHT / 2 
            starting_y = box_center_y - line_height 
            for i, title in enumerate(titles):
                t_title = gameFont['small'].render(title, False, (180, 0, 0))
                rect = t_title.get_rect(center=(WIDTH / 2, starting_y + i * line_height))
                if i == self.interfaceSelect:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                

                screen.blit(t_title, rect)