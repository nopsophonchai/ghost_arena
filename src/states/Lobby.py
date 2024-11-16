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
        self.option = 0 
        self.round = 0
        self.confirm = False
        self.select = 0
        self.enemiesList = []
        self.roundEnd = True
        self.player = Player()

        self.background_image = pygame.transform.scale(pygame.image.load("./graphics/shopBG1.png"), (WIDTH, HEIGHT))

    def Reset(self):
        self.option = 0
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
<<<<<<< HEAD

    def update(self, dt, events):
        self.player.render(dt)
        for event in events:
=======
    def update(self, dt, events):
       self.player.render(dt)
       for event in events:
>>>>>>> origin/main
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.option = (self.option - 1) % 3  # Cycle options left
                elif event.key == pygame.K_RIGHT:
                    self.option = (self.option + 1) % 3  # Cycle options right
                elif event.key == pygame.K_RETURN:
                    # Navigate based on selected option
                    if self.option == 0:
                        stateManager.Change('character', {'player': self.player, 'round': self.round})
                    elif self.option == 1:
                        stateManager.Change('shop', {'player': self.player, 'round': self.round})
                    elif self.option == 2:
                        stateManager.Change('select', {'player': self.player, 'round': self.round})

    def render(self, screen):
<<<<<<< HEAD
        scale_factor = 4.0  # Adjusted to make the character bigger 

        # Scale the player's current animation image
        scaled_image = pygame.transform.scale(
            self.player.currAni.image, 
            (int(self.player.currAni.image.get_width() * scale_factor),
             int(self.player.currAni.image.get_height() * scale_factor))
        )
        screen.blit(scaled_image, (WIDTH // 2 - scaled_image.get_width() // 2, HEIGHT // 2.5 - scaled_image.get_height() // 2))
        
        # Render the text options at the bottom of the screen
        self.draw_text_option(screen, "Characters", gameFont['medium'], WIDTH // 4, HEIGHT - 100, self.option == 0)
        self.draw_text_option(screen, "Shop", gameFont['medium'], WIDTH // 2, HEIGHT - 100, self.option == 1)
        self.draw_text_option(screen, "Play", gameFont['medium'], 3 * WIDTH // 4, HEIGHT - 100, self.option == 2, is_play=True)

    def draw_text_option(self, screen, text, font, x, y, is_selected, is_play=False):
        # Define the floating effect for the selected option
        y_offset = -15 if is_selected else 0  # Move up by 15 pixels if selected

        # Determine background color for the options
        if is_play:
            bg_color = (200, 0, 0) if not is_selected else (255, 50, 50)  # Brighter red for Play option when selected
        else:
            bg_color = (100, 100, 100) if is_selected else (0, 0, 0)  # Default background for other options

        # Render the text and its background with y-offset applied for floating effect
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x, y + y_offset))
        pygame.draw.rect(screen, bg_color, text_rect.inflate(30, 15), border_radius=10)  # Rounded rect background
        if is_selected and is_play:
            pygame.draw.rect(screen, (255, 255, 0), text_rect.inflate(40, 25), 3, border_radius=10)  # Yellow outline for selected Play
        screen.blit(text_surface, text_rect)
=======
        screen.blit(self.player.currAni.image,(WIDTH//2 - 64,HEIGHT//2 - 64,0,0))
        # screen.blit(pygame.image.load('graphics/swordCard.png'),(WIDTH//2-60,HEIGHT//1.5,0,0))

        self.player.items['sword'].render(screen,WIDTH//4,HEIGHT//1.5)
        self.player.items['Fire'].render(screen,WIDTH//1.5,HEIGHT//3)




        

>>>>>>> origin/main
