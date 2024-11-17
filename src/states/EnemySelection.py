from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *
from src.resources import *
from src.Player import Player
from src.Enemies.GongGoi import GongGoi
from src.Enemies.Preta import Preta
from src.Enemies.Phrai import Phrai
from src.Enemies.Krasue import Krasue
from src.Enemies.Monk import Monk
from src.Enemies.NangRam import NangRam
from src.Enemies.Faker import Faker
from src.Items.Rice import Rice
from src.Items.Fire import Fire
from src.Items.Water import Water
from src.Items.Card import Card
from src.Enemies.MaeNak import MaeNak,Dang
from src.Enemies.Ka import Ka


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

        self.choose = False
        self.itemList = ['Fire','Water','Rice','Armor']
        self.allEnemies = ['Preta','GongGoi']
        # self.allEnemies = ['MaeNak']
        # self.allEnemies = ['Ka']
        # self.allEnemies = ['NangRam']
        self.info = False


    def Reset(self):
        self.option = 1
        self.round = 0
        self.confirm = False
        self.select = 0

        self.enemiesList = []
        self.roundEnd = True
        self.player = None

        self.choose = False
        self.itemList = ['Fire','Water','Rice','Armor']
        self.allEnemies = ['Preta','GongGoi']

    def Exit(self):
        self.select = 0

    def Enter(self, params):
        self.player = params['player']
        if 'enemy' in params:
            self.enemy = params['enemy']
            self.enemy.ChangeAnimation(f'{self.enemy.name}Idle')
        print(f'Player Select Health: {self.player.health}')
        if 'round' in params:
            self.round = params['round']
        if self.roundEnd == True:
            self.player.health = self.player.maxHealth
            self.round += 1
            enemiesGenerated = rd.randint(min(self.round+3,6),6)
            match self.round:
                case 2:
                    self.allEnemies.append('Phrai')
                    self.allEnemies.append('Krasue')
                case 3:
                    self.allEnemies.append('NangRam')
                case 4:
                    self.allEnemies.append('MaeNak')
                case 5:
                    self.allEnemies.append('Ka')
                case 7:
                    self.allEnemies.append('Faker')
            
            # enemiesGenerated = 1

            for enemy in range(enemiesGenerated):
                selectedEnemy = rd.choice(self.allEnemies)
                addedEnemy = None
                match selectedEnemy:
                    case 'Preta': addedEnemy = Preta('Preta',(10+(2*(self.round-1))),(3+(self.round-1)))
                    case 'GongGoi': addedEnemy = GongGoi('GongGoi',(4+(2*(self.round-1))),(2+(self.round-1)))
                    case 'Phrai': addedEnemy = Phrai('Phrai',(6+(2*(self.round-1))),(3+(self.round-1)))
                    case 'Krasue': addedEnemy = Krasue('Krasue',(3+(2*(self.round-1))),(4+(self.round-1)))
                    case 'NangRam': addedEnemy = NangRam('Nang Ram',(8+(2*(self.round-1))),(4+(self.round-1)))
                    case 'MaeNak': addedEnemy = MaeNak('MaeNak',(8+(2*(self.round-1))),(4+(self.round-1)))
                    case 'Ka': addedEnemy = Ka('Ka',(8+(2*(self.round-1))),(2+(self.round-1)))
                    case 'Faker': addedEnemy = Faker('Faker',(8+(2*(self.round-1))),(2+(self.round-1)))
                    case 'Monk': addedEnemy = Monk('Monk',(80+(2*(self.round-1))),(10+(self.round-1)))
                addedEnemy.ChangeAnimation(f'{addedEnemy.name}Idle')
                self.enemiesList.append(addedEnemy)
            # print(self.enemiesList)
            if self.round == 7:
                self.enemiesList = [Faker('Faker',(8+(2*(self.round-1))),(2+(self.round-1)))]



            self.roundEnd = False
        else:
            for i in self.enemiesList:
                if i.isDead:
                    self.enemiesList.remove(i)
                    print(f'Removed {i}')
            # print(len(self.enemiesList))
            if len(self.enemiesList) == 0:
                self.roundEnd = True
                self.choose = True
                self.select = 0
                # stateManager.Change('lobby',{'player':self.player})


    def update(self, dt, events):
       # self.enemy.render(dt)
        if not self.choose:
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
                    if event.key == pygame.K_0:
                        if not self.info:
                            self.info = True
                        else:
                            self.info = False
            if self.confirm:
                payload = {'enemy':self.enemiesList[self.select],'round':self.round,'player':self.player}
                stateManager.Change('play',payload)
                self.confirm = False
        else:
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.select = (self.select - 1) % (len(self.itemList))
                        print(self.select)
                    if event.key == pygame.K_RIGHT:
                        self.select = (self.select + 1) % (len(self.itemList))
                        print(self.select)
                    if event.key == pygame.K_RETURN:
                        self.confirm = True
            if self.confirm:
                match self.itemList[self.select]:
                    case 'Fire': 
                        self.player.addItem(Fire('fire',self.player.damage,'Fire'))
                        self.itemList.remove(self.itemList[self.select])
                    case 'Water': 
                        self.player.addItem(Water('water',self.player.damage,'Water'))
                        self.itemList.remove(self.itemList[self.select])
                    case 'Rice': 
                        self.player.addItem(Rice('rice',self.player.damage,'Rice'))
                        self.itemList.remove(self.itemList[self.select])
                    case 'Armor': self.player.armor += 2
                self.choose = False
                self.confirm = False
                stateManager.Change('lobby',{'player':self.player,'round':self.round})
                
        for enemy in self.enemiesList:
            enemy.render(dt)
    def render(self, screen):
        
        if self.choose:
            item_spacing = 200
            total_width = item_spacing * (len(self.itemList) - 1)
            start_x = (WIDTH - total_width) / 2
            text_surface = gameFont['small'].render(f'Choose Your Item', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3))
            screen.blit(text_surface, rect)
            for i in range(len(self.itemList)):
                text_surface = gameFont['small'].render(f'{self.itemList[i]}', True, (255, 255, 255))
                rect = text_surface.get_rect(center=(start_x + item_spacing * i, HEIGHT / 1.25))
                if self.select == i:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                screen.blit(text_surface, rect)

        else:
        #show enemy     
            item_spacing = 200
            total_width = item_spacing * (len(self.enemiesList) - 1)
            start_x = (WIDTH - total_width) / 2
            #round info
            text_surface = gameFont['small'].render(f'Round {self.round}', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 5))
            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Press 0 to view enemy info', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 1.05))
            screen.blit(text_surface, rect)
            #animation of enemy 
            for i, enemy in enumerate(self.enemiesList):
                #enemy.render(dt)
                if enemy.currAni: 
                    enemy_image_rect =  enemy.currAni.image.get_rect(center=(start_x + item_spacing * i, HEIGHT / 2))
                    screen.blit(enemy.currAni.image, enemy_image_rect)
                else:
                    print("No animation")
                text_surface = gameFont['small'].render(self.enemiesList[i].name, True, (255, 255, 255))
                rect = text_surface.get_rect(center=(start_x + item_spacing * i, HEIGHT / 1.25))
                if self.select == i:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                screen.blit(text_surface, rect)

        if self.info:
            pygame.draw.rect(screen, (255, 255, 255), (WIDTH/2 - 200, HEIGHT/2 - 250, 400, 500))
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH/2 - 195, HEIGHT/2 - 245, 390, 490))
            text_surface = gameFont['medium'].render(f'{self.enemiesList[self.select].name}', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT /2 -220))
            screen.blit(text_surface, rect)

            y_offset = -160 
            for category, attacks in self.enemiesList[self.select].attacks.items():
                for attack in attacks:
                    y_offset += 20
                    attack_name = attack[1].capitalize()  # Attack name
                    attack_desc = attack[2]  # Attack description

                    # Render attack name
                    attack_name_surface = gameFont['small'].render(f'{attack_name}:', True, (255, 30, 30))
                    attack_name_rect = attack_name_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_offset))
                    screen.blit(attack_name_surface, attack_name_rect)
                    y_offset += 30  # Move down for the description

                    # Render attack description with line breaks
                    for line in attack_desc.split('\n'):
                        line_surface = gameFont['small'].render(line, True, (255, 255, 255))
                        line_rect = line_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_offset))
                        screen.blit(line_surface, line_rect)
                        y_offset += 30  # Move down for the next line
            