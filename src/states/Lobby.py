from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *
from src.resources import *
from src.Player import Player
from src.Enemies.GongGoi import GongGoi
from src.Enemies.Preta import Preta
pygame.font.init()
import random 

gameFont = {
    'small': pygame.font.Font('./fonts/font.ttf', 24),
    'medium': pygame.font.Font('./fonts/font.ttf', 48),
    'large': pygame.font.Font('./fonts/font.ttf', 96)
}

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 204, 255)

class Raindrop:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = 20

    def fall(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-HEIGHT, 0)
            self.x = random.randint(0, WIDTH)
            self.speed = 20 

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x - 1, self.y - 1, 3 + 2, 10 + 2))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 3, 10))
        pygame.draw.rect(screen, BLUE, (self.x + 1, self.y + 1, 3 - 2, 10 - 2))


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

        self.background_image = pygame.transform.scale(pygame.image.load("./graphics/lobby_background.jpeg"), (WIDTH, HEIGHT))

        # Menu options
        self.menu_options = ["Character", "Shop", "Play"]

        # Initialize raindrops
        self.raindrops = [Raindrop() for _ in range(30)]
        self.rain = pygame.mixer.Sound('sound/rain.mp3')

    def Reset(self):
        self.option = 0
        self.round = 0
        self.confirm = False
        self.select = 0
        self.enemiesList = []
        self.roundEnd = True
        self.player = Player()
        self.rain = pygame.mixer.Sound('sound/rain.mp3')
        print(self.player.damage)

    def Exit(self):
        self.rain.stop()

    def Enter(self, params):
        self.rain.play(-1) 
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
                sound = pygame.mixer.Sound('sound/hit.wav')
                sound.play()
                if event.key == pygame.K_UP:  # Move up in the menu
                    self.option = (self.option - 1) % len(self.menu_options)  # Cycle options upwards
                elif event.key == pygame.K_DOWN:  # Move down in the menu
                    self.option = (self.option + 1) % len(self.menu_options)  # Cycle options downwards
                elif event.key == pygame.K_RETURN:  # Select the current option
                    if self.option == 0:
                        stateManager.Change('character', {'player': self.player, 'round': self.round})
                    elif self.option == 1:
                        stateManager.Change('shop', {'player': self.player, 'round': self.round})
                    elif self.option == 2:
                        stateManager.Change('select', {'player': self.player, 'round': self.round})

        # Update raindrops
        for drop in self.raindrops:
            drop.fall()

    def render(self, screen):
        # Draw the background
        screen.blit(self.background_image, (0, 0))

        # Draw raindrops
        for drop in self.raindrops:
            drop.draw(screen)

        scale_factor = 2  
        scaled_width = int(self.player.currAni.image.get_width() * scale_factor)
        scaled_height = int(self.player.currAni.image.get_height() * scale_factor)
        scaled_image = pygame.transform.scale(self.player.currAni.image, (scaled_width, scaled_height))

        player_x_position = WIDTH // 4  
        player_y_position = HEIGHT // 2 - scaled_height // 2  
        screen.blit(scaled_image, (player_x_position, player_y_position))

        box_width = 300
        box_height = 70
        x_position = WIDTH // 2 + 200
        start_y = HEIGHT // 2 - (len(self.menu_options) * box_height) // 2  

        for i, option in enumerate(self.menu_options):
            y_position = start_y + i * (box_height + 30)  

            if i == self.option:
                bg_color = (255, 0, 0) if option == "Play" else (100, 100, 100)
                pygame.draw.rect(screen, bg_color, (x_position, y_position, box_width, box_height))

                pygame.draw.rect(screen, (255, 255, 255), (x_position - 5, y_position - 5, box_width + 10, box_height + 10), 3)
            else:
                bg_color = (10, 52, 99) if option == "Play" else (50, 50, 50)
                pygame.draw.rect(screen, bg_color, (x_position, y_position, box_width, box_height))

            option_text = gameFont['medium'].render(option, True, (255, 255, 255))
            text_x = x_position + (box_width - option_text.get_width()) // 2
            text_y = y_position + (box_height - option_text.get_height()) // 2
            screen.blit(option_text, (text_x, text_y))
