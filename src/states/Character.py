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
        'super_small': pygame.font.Font('./fonts/font.ttf', 21),
        'super_small': pygame.font.Font('./fonts/font.ttf', 21),
        'small': pygame.font.Font('./fonts/font.ttf', 24),
        'medium': pygame.font.Font('./fonts/font.ttf', 30),
        'medium': pygame.font.Font('./fonts/font.ttf', 30),
        'large': pygame.font.Font('./fonts/font.ttf', 96)
}
class Character(BaseState):
    def __init__(self):
        super(Character, self).__init__()
        #start = 1,       ranking = 2
        self.option = 1
        self.round = 0
        self.confirm = False
        self.select = 0

        self.enemiesList = []
        self.roundEnd = True
        self.player = Player()
        self.page = 1

        self.midBattle = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.selected_item_index = 0

        self.bg_image = pygame.image.load("./graphics/wall.png")

        self.bg_image = pygame.transform.scale(
            self.bg_image, (WIDTH+5, HEIGHT+5))
        
        self.image1 = pygame.image.load('graphics/mirrorr.png')
        self.image1 = pygame.transform.scale(self.image1,(650,650))

        self.image2 = pygame.image.load('graphics/frame.png')
        self.image2 = pygame.transform.scale(self.image2,(495,550))

        self.image3 = pygame.image.load('graphics/skeleton_point_right.png')
        self.image3 = pygame.transform.scale(self.image3,(70,70))

        self.image4 = pygame.image.load('graphics/up_arrow.png')
        self.image4 = pygame.transform.scale(self.image4,(30,30))

        self.image5 = pygame.image.load('graphics/down_arrow.png')
        self.image5 = pygame.transform.scale(self.image5,(30,30))

        self.image6 = pygame.image.load('graphics/black.jpg')
        self.image6 = pygame.transform.scale(self.image6,(200,340))    

        self.midBattle = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.selected_item_index = 0

        self.bg_image = pygame.image.load("./graphics/wall.png")

        self.bg_image = pygame.transform.scale(
            self.bg_image, (WIDTH+5, HEIGHT+5))
        
        self.image1 = pygame.image.load('graphics/mirrorr.png')
        self.image1 = pygame.transform.scale(self.image1,(650,650))

        self.image2 = pygame.image.load('graphics/frame.png')
        self.image2 = pygame.transform.scale(self.image2,(495,550))

        self.image3 = pygame.image.load('graphics/skeleton_point_right.png')
        self.image3 = pygame.transform.scale(self.image3,(70,70))

        self.image4 = pygame.image.load('graphics/up_arrow.png')
        self.image4 = pygame.transform.scale(self.image4,(30,30))

        self.image5 = pygame.image.load('graphics/down_arrow.png')
        self.image5 = pygame.transform.scale(self.image5,(30,30))

        self.image6 = pygame.image.load('graphics/black.jpg')
        self.image6 = pygame.transform.scale(self.image6,(200,340))    

        self.bgmusic = pygame.mixer.Sound('sound/character.mp3')

    def Reset(self):
        self.option = 1
        self.round = 0
        self.confirm = False
        self.select = 0

        self.enemiesList = []
        self.roundEnd = True
        self.player = Player()
        self.bgmusic = pygame.mixer.Sound('sound/character.mp3')
        self.page = 1

    def Exit(self):
        self.bgmusic.stop()
        pass

    def Enter(self, params):
        self.bgmusic.play(-1)
        if 'player' in params:
            self.player = params['player']
            
        if 'midBattle' in params:
            self.midBattle = True
        else:
            self.midBattle = False
        if 'round' in params:
            self.round = params['round']
        self.player.ChangeAnimation('playerIdle')
    def update(self, dt, events):
       self.player.render(dt)
       self.player.render(dt)
       for event in events:
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                sound = pygame.mixer.Sound('sound/hit.wav')
                sound.play()
                if event.key == pygame.K_RIGHT:
                    if self.midBattle:
                        stateManager.Change('play',{})
                    else:
                        stateManager.Change('lobby',{'player': self.player})
                    if self.midBattle:
                        stateManager.Change('play',{})
                    else:
                        stateManager.Change('lobby',{'player': self.player})
                if event.key == pygame.K_UP:
                    self.page += 1
                elif event.key == pygame.K_UP:
                    #self.page += 1
                    self.selected_item_index = (self.selected_item_index - 1) % len(self.player.items)
                    print(self.player.items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item_index = (self.selected_item_index + 1) % len(self.player.items)
              
                elif event.key == pygame.K_UP:
                    #self.page += 1
                    self.selected_item_index = (self.selected_item_index - 1) % len(self.player.items)
                    print(self.player.items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item_index = (self.selected_item_index + 1) % len(self.player.items)
              
    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        # text_surface = gameFont['small'].render(f'Max Health: {self.player.health}', True, (255, 255, 255))
        # rect = text_surface.get_rect(center=(WIDTH / 4, HEIGHT / 3))
        # screen.blit(text_surface, rect)
        # text_surface = gameFont['small'].render(f'Damage: {self.player.damage}', True, (255, 255, 255))
        # rect = text_surface.get_rect(center=(WIDTH / 4, HEIGHT / 2.5))
        # screen.blit(text_surface, rect)
        # text_surface = gameFont['small'].render(f"Items", True, (255, 255, 255))
        # rect = text_surface.get_rect(center=(WIDTH / 1.5, HEIGHT / 5.5))
        # screen.blit(text_surface, rect)
        # text_surface = gameFont['small'].render(f'Max Health: {self.player.health}', True, (255, 255, 255))
        # rect = text_surface.get_rect(center=(WIDTH / 4, HEIGHT / 3))
        # screen.blit(text_surface, rect)
        # text_surface = gameFont['small'].render(f'Damage: {self.player.damage}', True, (255, 255, 255))
        # rect = text_surface.get_rect(center=(WIDTH / 4, HEIGHT / 2.5))
        # screen.blit(text_surface, rect)
        # text_surface = gameFont['small'].render(f"Items", True, (255, 255, 255))
        # rect = text_surface.get_rect(center=(WIDTH / 1.5, HEIGHT / 5.5))
        # screen.blit(text_surface, rect)

        text_surface = gameFont['medium'].render(f'Max Health: {self.player.maxHealth}', True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH /3 - 45, HEIGHT / 4))
        screen.blit(text_surface, rect)

        text_surface = gameFont['medium'].render(f'Damage: {self.player.damage}', True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH / 3 - 45, HEIGHT /4 + 40))
        screen.blit(text_surface, rect)

        text_surface = gameFont['medium'].render(f'Armor: {self.player.armor}', True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH / 3 - 45, HEIGHT /4 + 80))
        screen.blit(text_surface, rect)

        text_surface = gameFont['super_small'].render(f'Press right to go back', True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH / 2 + 350, HEIGHT /4 + 480))
        screen.blit(text_surface, rect)

        items_text_surface = gameFont['medium'].render("Items", True, (255, 255, 255))
        items_rect = items_text_surface.get_rect(center=(WIDTH / 2 + 135, HEIGHT / 5.5 + 50))
        screen.blit(items_text_surface, items_rect)

        scale_factor = 1  # Adjust to desired size
        scaled_image = pygame.transform.scale(
            self.player.currAni.image, 
            (
                int(self.player.currAni.image.get_width() * scale_factor),
                int(self.player.currAni.image.get_height() * scale_factor)
            )
        )

        # Blit the scaled image
        

        screen.blit(self.image1, (50, 240)) 
        screen.blit(self.image2, (700, 80))
        screen.blit(self.image3, (WIDTH / 2 + 490, HEIGHT /4 + 435))
        screen.blit(self.image4, (WIDTH - 590 , HEIGHT /2))
        screen.blit(self.image5, (WIDTH - 100, HEIGHT /2))
        
        screen.blit(scaled_image, (255, 395))
        # Display only the selected item
        # if self.selected_item_index == 0:
        #     self.player.items['sword'].render(screen, WIDTH // 2 + 140, HEIGHT / 2 - 120)
        # elif self.selected_item_index == 1:
        #     self.player.items['Fire'].render(screen, WIDTH // 2 + 140, HEIGHT / 2 - 120)\
        list(self.player.items.values())[self.selected_item_index].render(screen, WIDTH // 2 + 140, HEIGHT / 2 - 120)
