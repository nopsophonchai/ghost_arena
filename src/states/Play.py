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
        self.checkCharacter = False
        self.bgmusic = pygame.mixer.Sound('sound/fightmusic.MP3')

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

        self.checkCharacter = False
        self.bgmusic = pygame.mixer.Sound('sound/fightmusic.MP3')



    def Exit(self):
        self.bgmusic.stop()
        self.monkRound = False
        if not self.checkCharacter:
            self.player.refresh()



    def Enter(self, params):
        self.bgmusic.play(-1)
        if not self.checkCharacter:
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
        # print(self.player.damage)
        self.player.render(dt)
        self.enemy.render(dt)
        self.player.updateEffects(dt)
        self.enemy.updateEffects(dt)
        if self.player.health <= 0:
            self.checkCharacter = False
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
                        sound = pygame.mixer.Sound('sound/hit.wav')
                        sound.play()
                        if event.key == pygame.K_LEFT:
                            self.select = (self.select - 1) % (len(self.player.current) + 2)
                            # print(self.select)
                        if event.key == pygame.K_RIGHT:
                            self.select = (self.select + 1) % (len(self.player.current) + 2)
                            # print(self.select)
                        if event.key == pygame.K_RETURN:
                            self.confirm = True
                        if event.key == pygame.K_0:
                            self.checkCharacter = True
                            stateManager.Change('character',{'midBattle':True,'player':self.player})

            if self.confirm:
                self.confirmHandle(dt, events)
        else:
            self.select = 0
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
                # print(self.player.health)
                # print(self.enemy.maxHealth//2)
                # print(self.player.health + (self.enemy.maxHealth // 2))
                # print(min(self.player.maxHealth,self.player.health + (self.enemy.maxHealth // 2)))
                # self.player.health = min(self.player.maxHealth,self.player.health + (self.enemy.maxHealth // 2))
                # # print(self.player.health)
                # self.player.gold += self.enemy.gold + (self.round*2)

    def confirmHandle(self,dt, events):
        print(f'Self Interface: {self.interface}')
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
                    sound = pygame.mixer.Sound('sound/hit.wav')
                    sound.play()
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
                            self.player.addEffect('Block!',(WIDTH / 3, HEIGHT / 6), duration=100)
                            self.enemy.buffs.append(sun)
                elif chosenCard.item.type == 'Spell':
                    chosenCard.item.attack(self.enemy,self.player,self.interfaceSelect)



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
                if self.enemy.health <= 0 and self.enemy.name != 'Dang':
                    # print(self.enemy.health)
                    self.enemy.isDead = True
                    self.deadTimer = 120
                    # print(self.enemy.health)
                    self.player.health = min(self.player.maxHealth,self.player.health + (self.enemy.maxHealth // 2))
                    # print(self.player.health)
                    self.player.gold += self.enemy.gold + (self.round*2)
                elif self.enemy.health <= 0 and self.enemy.name == 'Dang':
                    self.enemy.isDead = True
                    self.enemy = self.thisNak
                    self.enemy.dangFlag = False  
                

    def render(self, screen):
        # screen.blit(pygame.image.load('graphics/fightbg.png'),(0,-150,0,0))
        fight_bg = pygame.image.load('graphics/fightbg.png')
        crop_rect = pygame.Rect(0, 150, fight_bg.get_width(), fight_bg.get_height() - 150)
        cropped_fight_bg = fight_bg.subsurface(crop_rect)
        screen.blit(cropped_fight_bg, (0, 0))
        pygame.draw.rect(screen,(255,255,255),(0,HEIGHT//1.25-5,WIDTH,HEIGHT-HEIGHT//1.25))
        pygame.draw.rect(screen,(0,0,0),(0,HEIGHT//1.25,WIDTH,HEIGHT-HEIGHT//1.25))
        playerRect = self.player.currAni.image.get_rect(center=(WIDTH / 3, HEIGHT / 2.5))
        enemyRect = self.enemy.currAni.image.get_rect(center=(WIDTH / 1.5, HEIGHT / 2.5))
        screen.blit(self.player.currAni.image,playerRect)
        screen.blit(self.enemy.currAni.image,enemyRect)

        pygame.draw.rect(screen,(255,255,255),(WIDTH//1.25,HEIGHT // 1.5,(WIDTH - WIDTH//1.25),(HEIGHT - HEIGHT // 1.5)))
        pygame.draw.rect(screen,(0,0,0),(WIDTH//1.25 + 5,HEIGHT // 1.5 + 5,(WIDTH - WIDTH//1.25) - 10,(HEIGHT - HEIGHT // 1.5) - 10))

        for i in range(len(self.player.statusList)):
            screen.blit(pygame.image.load(self.player.statusList[i][1]),(WIDTH/5,HEIGHT/4 + (60*i),45,45))
        for i in range(len(self.enemy.statusList)):
            screen.blit(pygame.image.load(self.enemy.statusList[i][1]),(WIDTH/1.35,HEIGHT/4 + (60*i),45,45))


        addOffset((WIDTH / 7, HEIGHT / 6),2,f'Your Damage: {self.player.damage}',screen)
        message_surface = gameFont['small'].render(f'Your Damage: {self.player.damage}', True, (255, 215, 0))
        message_rect = message_surface.get_rect(center=(WIDTH / 7, HEIGHT / 6))
        screen.blit(message_surface, message_rect)

        addOffset((WIDTH / 7, HEIGHT / 4.8),2,f'Your Armor: {self.player.armor}',screen)
        message_surface = gameFont['small'].render(f'Your Armor: {self.player.armor}', True, (255, 215, 0))
        message_rect = message_surface.get_rect(center=(WIDTH / 7, HEIGHT / 4.8))
        screen.blit(message_surface, message_rect)

        addOffset((WIDTH / 1.2, HEIGHT / 6),2,f'Enemy Damage: {self.enemy.damage}',screen)
        message_surface = gameFont['small'].render(f'Enemy Damage: {self.enemy.damage}', True, (255, 215, 0))
        message_rect = message_surface.get_rect(center=(WIDTH / 1.2, HEIGHT / 6))
        screen.blit(message_surface, message_rect)

        addOffset((WIDTH / 1.2, HEIGHT / 4.8),2,f'Enemy Armor: {self.enemy.armor}',screen)
        message_surface = gameFont['small'].render(f'Enemy Armor: {self.enemy.armor}', True, (255, 215, 0))
        message_rect = message_surface.get_rect(center=(WIDTH / 1.2, HEIGHT / 4.8))
        screen.blit(message_surface, message_rect)

        if self.deadTimer > 0:
            if not self.monkRound:
                screen.fill((0,0,0))
                message_surface = gameFont['small'].render(f'You have defeated {self.enemy.name}!', True, (255, 215, 0))
                message_rect = message_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3))
                screen.blit(message_surface, message_rect)
                message_surface = gameFont['small'].render(f'Gold earned {self.enemy.gold+(2*self.round)}!', True, (255, 215, 0))
                message_rect = message_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                screen.blit(message_surface, message_rect)
                message_surface = gameFont['small'].render(f'Health recovered {self.enemy.maxHealth // 2}!', True, (255, 215, 0))
                message_rect = message_surface.get_rect(center=(WIDTH / 2, HEIGHT / 1.8))
                screen.blit(message_surface, message_rect)
                self.deadTimer -= 1
                if self.deadTimer <= 0:
                    self.called = 0
                    self.checkCharacter = False
                    if self.enemy.name != 'Faker':
                        stateManager.Change('select',{'player':self.player})
                    else:
                        stateManager.Change('gameover',{'victory':True})
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
                addOffset((WIDTH / 1.5, HEIGHT / 3.25),2,f"{self.thisNak.name}: {self.thisNak.health}",screen)
                t_title = gameFont['small'].render(f"{self.thisNak.name}: {self.thisNak.health}", False, (255, 10, 40))
                rect = t_title.get_rect(center=(WIDTH / 1.5, HEIGHT / 3.25))
                screen.blit(t_title,rect)
            addOffset((WIDTH / 1.5, HEIGHT / 5),2,f"{self.enemy.name}: {self.enemy.health}",screen)
            t_title = gameFont['small'].render(f"{self.enemy.name}: {self.enemy.health}", False, (255, 10, 40))
            # print(self.enemy.name)
            rect = t_title.get_rect(center=(WIDTH / 1.5, HEIGHT / 5))
            screen.blit(t_title, rect)

            addOffset((WIDTH / 3, HEIGHT / 5),2,f"Player Health {self.player.health}",screen)
            t_title = gameFont['small'].render(f"Player Health {self.player.health}", False, (255, 255, 255))
            rect = t_title.get_rect(center=(WIDTH / 3, HEIGHT / 5))
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
                    # print(card_x)
                    if i + 1 == self.select:
                        # Card is selected
                        if (self.player.current[i].item.weaponType == 'melee' and self.player.noMelee) or (self.player.current[i] == self.lastCard and self.player.noCard):
                            # Display "Disabled" message if conditions are met
                            if self.enemy.name == 'Ka':
                                t_title = gameFont['small'].render("KA", False, (80, 80, 80))
                                rect = t_title.get_rect(center=(card_x+40, HEIGHT / 1.25))
                                screen.blit(t_title, rect)
                            else:
                                t_title = gameFont['small'].render("Disabled!", False, (80, 80, 80))
                                rect = t_title.get_rect(center=(card_x+60, HEIGHT / 1.125))
                                screen.blit(t_title, rect)
                        else:
                            # Display the card normally
                            if self.enemy.name == 'Ka':
                                t_title = gameFont['small'].render("KA", False, (0, 123, 255))
                                rect = t_title.get_rect(center=(card_x+40, HEIGHT / 1.25))
                                screen.blit(t_title, rect)
                            else:
                                right_area_start = WIDTH // 1.25
                                right_area_width = WIDTH - right_area_start
                                text_x_center = right_area_start + right_area_width // 2
                                self.player.current[i].render(screen, card_x, HEIGHT / 1.6)
                                t_title = gameFont['medium'].render(f"{self.player.current[i].name.upper()}", False, (255, 255, 255))
                                rect = t_title.get_rect(center=(text_x_center, HEIGHT / 1.4))
                                screen.blit(t_title, rect)
                                t_title = gameFont['small'].render(f"Damage: {self.player.current[i].item.damage}", False, (255, 255, 255))
                                rect = t_title.get_rect(center=(text_x_center, HEIGHT / 1.25))
                                screen.blit(t_title, rect)
                    else:
                        # Card is not selected
                        if self.enemy.name == 'Ka':
                            t_title = gameFont['small'].render("KA", False, (255, 255, 255))
                            rect = t_title.get_rect(center=(card_x+40, HEIGHT / 1.125))
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
        
        outline_color = (0, 0, 0) 
        offset = 2  

        for action in self.player.effectList:
            text_surface = gameFont['small'].render(action['text'], True, action['color'])
            position = action['position']
            outline_positions = [
                (position[0] - offset, position[1] - offset),  
                (position[0] + offset, position[1] - offset),  
                (position[0] - offset, position[1] + offset),  
                (position[0] + offset, position[1] + offset),  
                (position[0] - offset, position[1]),           
                (position[0] + offset, position[1]),           
                (position[0], position[1] - offset),           
                (position[0], position[1] + offset)            
            ]

            for outline_pos in outline_positions:
                outline_surface = gameFont['small'].render(action['text'], True, outline_color)
                screen.blit(outline_surface, outline_pos)

            screen.blit(text_surface, position)


        for action in self.enemy.effectList:
            text_surface = gameFont['small'].render(action['text'], True,action['color'])
            position = action['position']
            outline_positions = [
                (position[0] - offset, position[1] - offset),  
                (position[0] + offset, position[1] - offset),  
                (position[0] - offset, position[1] + offset),  
                (position[0] + offset, position[1] + offset),  
                (position[0] - offset, position[1]),           
                (position[0] + offset, position[1]),           
                (position[0], position[1] - offset),           
                (position[0], position[1] + offset)            
            ]

            for outline_pos in outline_positions:
                outline_surface = gameFont['small'].render(action['text'], True, outline_color)
                screen.blit(outline_surface, outline_pos)
            screen.blit(text_surface,  position)


def addOffset(position,offset,text,screen):
    outline_positions = [
                (position[0] - offset, position[1] - offset),  
                (position[0] + offset, position[1] - offset),  
                (position[0] - offset, position[1] + offset),  
                (position[0] + offset, position[1] + offset),  
                (position[0] - offset, position[1]),           
                (position[0] + offset, position[1]),           
                (position[0], position[1] - offset),           
                (position[0], position[1] + offset)            
            ]
    for outline_pos in outline_positions:
        outline_surface = gameFont['small'].render(text, True, (0,0,0))
        outlinePosition = outline_surface.get_rect(center=outline_pos)
        screen.blit(outline_surface, outlinePosition)