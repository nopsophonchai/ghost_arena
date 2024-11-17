from src.states.BaseState import BaseState
import pygame, sys
from src.Items.Debuff import Debuff
from src.constants import *
from src.Dependency import *
from src.resources import *
from src.Player import Player
from src.Enemies.GongGoi import GongGoi
from src.Enemies.Preta import Preta
from src.Enemies.MaeNak import MaeNak, Dang
from src.Items.Card import Card
from src.Items.Weapon import Weapon

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

        self.called = 0

        self.lastCard = None
        self.disableCard = False

        self.dang = False
        self.thisNak = None

        self.monkRound = False

        self.blood_animation = sprite_collection['slash'].animation
        self.fire_animation = sprite_collection['explosion'].animation
        self.bg_image = pygame.image.load("./graphics/bg_lobby.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.top_frame = pygame.image.load("./graphics/top_frame.png")
        self.big_frame = pygame.image.load("./graphics/big_frame.png")
        self.top_frame = pygame.transform.scale(self.top_frame, (200, 100))
        self.big_frame = pygame.transform.scale(self.big_frame, (300, 300))

        self.spell = False


    def Reset(self):
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

        self.called = 0

        self.lastCard = None
        self.disableCard = False

        self.dang = False
        self.thisNak = None

        self.monkRound = False


    def Exit(self):
        self.player.refresh()


    def Enter(self, params):
        self.player = params['player']
        for i in range(3):
            self.player.drawCard()
        self.enemy = params['enemy']
        self.enemy.ChangeAnimation(f'{self.enemy.name}Idle')
        if 'round' in params:
            self.round = params['round']
        if self.enemy.name == 'Monk':
            self.monkRound = True

        self.turn = 0
        # print(self.player)



    def update(self, dt, events):
        self.blood_animation.update(dt)
        self.fire_animation.update(dt)
        self.player.render(dt)
        self.enemy.render(dt)
        if self.player.health <= 0:
            stateManager.Change('gameover',{})
        if self.turn == 0:
            if self.player.currAni.times_played > 0:
                self.player.currAni.Refresh()
                self.player.ChangeAnimation('playerIdle')
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
                            # print(self.select)
                        if event.key == pygame.K_RIGHT:
                            self.select = (self.select + 1) % (len(self.player.current) + 2)
                            # print(self.select)
                        if event.key == pygame.K_RETURN:
                            self.confirm = True

            if self.confirm:
                self.confirmHandle(dt, events)
        else:
            if self.enemy.currAni.times_played > 0:
                self.enemy.currAni.Refresh()
                self.enemy.ChangeAnimation(f'{self.enemy.name}Idle')
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
                    self.player.currAni.Refresh()
                    self.player.ChangeAnimation('playerHurt')
                    self.player.currAni.loop = False

                        
                    if self.enemy.name == 'MaeNak':
                        if self.enemy.dangFlag:
                            self.thisNak = self.enemy
                            self.enemy = Dang('Dang',(3+(2*(self.round-1))),(4+(self.round-1)),self.thisNak)
                            self.enemy.ChangeAnimation('DangIdle')
                    self.turn = 0
                    self.turnCount = 0
                    self.buffCount = 0
                    self.turnTimer = 0
                    # print("-------Player's Turn-------")
            elif self.called != 1 and self.enemy.name != 'Dang':
                self.called = 1
                self.deadTimer = 120
                        # print(self.enemy.health)
                self.player.health = min(self.player.maxHealth,self.player.health + (self.enemy.maxHealth // 2))
                # print(self.player.health)
                self.player.gold += self.enemy.gold + (self.round*2)

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
                # print(self.player.noMelee)
                if self.player.current[self.select-1].item.weaponType == 'melee' and self.player.noMelee:
                    pass
                elif self.player.current[self.select-1] == self.lastCard and self.player.noCard:
                    print('No card')
                    pass
                else:
                    chosenCard = self.player.current[self.select-1]
                    if not self.player.noCard:
                        self.lastCard = chosenCard
                        print(f'Last Card: {self.lastCard.name}')
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
                            # print("-------Enemy's Turn-------")
                    if chosenCard.item.type == 'Spell':
                        self.interface = True
                        self.confirm = True

                    if self.enemy.health <= 0 and self.enemy.name != 'Dang':
                        self.enemy.isDead = True
                        self.deadTimer = 120
                        # print(self.enemy.health)
                        self.player.health = min(self.player.maxHealth,self.player.health + (self.enemy.maxHealth // 2))
                        # print(self.player.health)
                        self.player.gold += self.enemy.gold + (self.round*2)
                    if self.enemy.health <= 0 and self.enemy.name == 'Dang':
                        self.enemy.isDead = True
                        self.enemy = self.thisNak
                        self.enemy.dangFlag = False

                        
                    
        else:
            # print("Welcome to the show")
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
                if chosenCard.item.type == 'Weapon':
                    match self.interfaceSelect:  
                        case 0: chosenCard.use(self.enemy,self.player)
                        case 1: chosenCard.heal(self.player,int(chosenCard.item.damage // 2))
                        case 2: 
                            def apply(target):
                                target.miss = True
                                # print(f'Changed Miss: {target.miss}')
                            def remove(target):
                                target.miss = False
                            sun = Debuff('sun',apply,remove,2)
                            self.enemy.buffs.append(sun)
                elif chosenCard.item.type == 'Spell':
                    chosenCard.item.attack(self.enemy,self.player,self.interfaceSelect)
                    self.spell = True
                  



                self.player.useCard(self.player.current[self.select-1])
                self.interface = False
                self.interfaceConfirm = False
                self.confirm = False
                self.turn = 1   
                self.turnCount = 0
                self.drawCount = 0
                if len(self.player.current)==0:
                    self.select = 0
                # print("-------Enemy's Turn-------")
                # print(f'Enemy Health:{self.enemy.health}')
                if self.enemy.health <= 0:
                    # print(self.enemy.health)
                    self.enemy.isDead = True
                    self.deadTimer = 120
                    # print(self.enemy.health)
                    self.player.health = min(self.player.maxHealth,self.player.health + (self.enemy.maxHealth // 2))
                    # print(self.player.health)
                    self.player.gold += self.enemy.gold + (self.round*2)
                

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))

        # vfx here my friends
        original_image = self.blood_animation.image
        original_width, original_height = original_image.get_size()
        new_width = int(original_width * 3)  
        new_height = int(original_height * 3)  
        scaled_image = pygame.transform.scale(original_image, (new_width, new_height))
        if self.enemy.cry == True:
            screen.blit(scaled_image, (WIDTH / 1.5, HEIGHT / 3.75,0,0))
            self.enemy.cry = False
        
        screen.blit(self.player.currAni.image,(WIDTH / 3.5, HEIGHT / 3.75,0,0))
        screen.blit(self.enemy.currAni.image,(WIDTH / 1.5, HEIGHT / 3.75,0,0))

        screen.blit(self.big_frame, (WIDTH//1.3-7,HEIGHT // 1.5))
        #pygame.draw.rect(screen,(80,80,80),(WIDTH//1.25,HEIGHT // 1.5,400,400))


        if self.deadTimer > 0:
            if not self.monkRound:
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
                    self.called = 0
                    stateManager.Change('select',{'player':self.player})
            else:
                message_surface = gameFont['small'].render(f'You have defeated {self.enemy.name}!', True, (255, 215, 0))
                message_rect = message_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                screen.blit(message_surface, message_rect)
                message_surface = gameFont['small'].render(f'ALL ITEMS ARE FREE!', True, (255, 215, 0))
                message_rect = message_surface.get_rect(center=(WIDTH / 2, HEIGHT / 1.5))
                screen.blit(message_surface, message_rect)
                self.deadTimer -= 1
                if self.deadTimer <= 0:
                    self.called = 0
                    stateManager.Change('shop',{'player':self.player,'free':True})
        else:
            
            if self.enemy.name == 'Dang':
                t_title = gameFont['small'].render(f"{self.thisNak.name}: {self.thisNak.health}", False, (255, 10, 40))
                rect = t_title.get_rect(topright=(WIDTH -10,10))
                screen.blit(t_title,rect)
            t_title = gameFont['small'].render(f"{self.enemy.name}: {self.enemy.health}", False, (255, 10, 40))
            # print(self.enemy.name)
            rect = t_title.get_rect(topleft=(WIDTH /1.5 + 90,60))
            screen.blit(self.top_frame, (WIDTH /1.5 +30,10))
            screen.blit(t_title, rect)
            t_title = gameFont['small'].render(f"Player Health: {self.player.health}", False, (255, 255, 255))
            rect = t_title.get_rect(topleft=(10,10))
            screen.blit(t_title, rect)


            if self.turn == 0:
                card_width = 120
                num_cards = len(self.player.current)
                reserved_width = WIDTH * 0.4
                available_width = WIDTH - reserved_width
                spacing = 10  # Minimum spacing of 20 pixels

                # Calculate the starting x position for centering within the available width
                start_x = reserved_width / 2

                # Render each card within the 75% width area
                for i in range(num_cards):
                    
                    card_x = start_x + (i * (card_width + spacing))  # Add extra spacing for the first card
                    print(card_x)
                    if i + 1 == self.select:
                        # Card is selected
                        if (self.player.current[i].item.weaponType == 'melee' and self.player.noMelee) or (self.player.current[i] == self.lastCard and self.player.noCard):
                            # Display "Disabled" message if conditions are met
                            if self.enemy.name == 'Ka':
                                t_title = gameFont['small'].render("KA", False, (80, 80, 80))
                                rect = t_title.get_rect(center=(card_x, HEIGHT / 1.125))
                                screen.blit(t_title, rect)
                            else:
                                t_title = gameFont['small'].render("Disabled!", False, (80, 80, 80))
                                rect = t_title.get_rect(center=(card_x+60, HEIGHT / 1.125))
                                screen.blit(t_title, rect)
                        else:
                            # Display the card normally
                            if self.enemy.name == 'Ka':
                                t_title = gameFont['small'].render("KA", False, (0, 123, 255))
                                rect = t_title.get_rect(center=(card_x, HEIGHT / 1.6))
                                screen.blit(t_title, rect)
                            else:
                                right_area_start = WIDTH // 1.25
                                right_area_width = WIDTH - right_area_start
                                text_x_center = right_area_start + right_area_width // 2
                                self.player.current[i].render(screen, card_x, HEIGHT / 1.6)
                                t_title = gameFont['medium'].render(f"{self.player.current[i].name.upper()}", False, (139, 0, 0))
                                rect = t_title.get_rect(center=(text_x_center-35, HEIGHT / 1.4+55))
                                screen.blit(t_title, rect)
                                t_title = gameFont['small'].render(f"Damage: {self.player.current[i].item.damage}", False, (0, 0, 0))
                                rect = t_title.get_rect(center=(text_x_center-35, HEIGHT / 1.25+55))
                                screen.blit(t_title, rect)
                    else:
                        # Card is not selected
                        if self.enemy.name == 'Ka':
                            t_title = gameFont['small'].render("KA", False, (255, 255, 255))
                            rect = t_title.get_rect(center=(card_x, HEIGHT / 1.5))
                            screen.blit(t_title, rect)
                        else:
                            self.player.current[i].render(screen, card_x, HEIGHT / 1.5)

                # Draw "Draw Card" and "End Turn" options with appropriate spacing
                draw_card_x = start_x - 70
                end_turn_x = start_x + num_cards * (card_width + spacing) + 60

                # Draw "Draw Card"
                if self.select == 0:
                    t_title = gameFont['small'].render("Draw Card", False, (0, 123, 56))
                    rect = t_title.get_rect(center=(draw_card_x, HEIGHT / 1.25))
                    screen.blit(t_title, rect)
                else:
                    t_title = gameFont['small'].render("Draw Card", False, (30, 255, 30))
                    rect = t_title.get_rect(center=(draw_card_x, HEIGHT / 1.125))
                    screen.blit(t_title, rect)

                # Draw "End Turn"
                if self.select == (num_cards + 1):
                    t_title = gameFont['small'].render("End Turn", False, (180, 0, 0))
                    rect = t_title.get_rect(center=(end_turn_x, HEIGHT / 1.25))
                    screen.blit(t_title, rect)
                else:
                    t_title = gameFont['small'].render("End Turn", False, (180, 0, 0))
                    rect = t_title.get_rect(center=(end_turn_x, HEIGHT / 1.125))
                    screen.blit(t_title, rect)
                    

        if self.interface:
            if self.player.current[self.select-1].item.type == 'Weapon':
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
            elif self.player.current[self.select-1].item.type == 'Spell':
                pygame.draw.rect(screen, (255, 255, 255), (WIDTH/2 - 150, HEIGHT/2 - 150, 300, 300))
                pygame.draw.rect(screen, (0, 0, 0), (WIDTH/2 - 145, HEIGHT/2 - 145, 290, 290))
                titles = [i[0] for i in self.player.current[self.select-1].item.spellList]
                line_height = 50 
                box_center_y = HEIGHT / 2 
                starting_y = box_center_y - line_height 
                for i, title in enumerate(titles):
                    t_title = gameFont['small'].render(title, False, (180, 0, 0))
                    rect = t_title.get_rect(center=(WIDTH / 2, starting_y + i * line_height))
                    if i == self.interfaceSelect:
                        pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                    

                    screen.blit(t_title, rect)