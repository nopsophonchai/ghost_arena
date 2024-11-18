from src.states.BaseState import BaseState
import pygame, sys, random
from ..Dependency import *
from src.states.Play import Play
from src.states.Lobby import Lobby
from src.states.EnemySelection import EnemySelection
from src.states.GameOver import GameOver
from src.states.Character import Character
from src.states.Shop import Shop

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 204, 255)

class Raindrop:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = 10  

    def fall(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-HEIGHT, 0)
            self.x = random.randint(0, WIDTH)
            self.speed = 10  

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x - 1, self.y - 1, 3 + 2, 10 + 2))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 3, 10))
        pygame.draw.rect(screen, BLUE, (self.x + 1, self.y + 1, 3 - 2, 10 - 2))

class StartState(BaseState):
    def __init__(self):
        super(StartState, self).__init__()
        self.option = 1
        self.showNum = False
        self.raindrops = [Raindrop() for _ in range(100)]  
        self.lightning_active = False
        self.lightning_flash_count = 0
        self.lightning_timer = 0
        self.lightning_cooldown = random.randint(200, 500)  
        self.lightning_alpha = 255  
        self.mainScreen = False

        self.introTimer = 0
        self.rain = pygame.mixer.Sound('sound/rain.mp3')

    def Reset(self):
        self.option = 1
        self.showNum = False

    def Exit(self):
        self.rain.stop()
        pygame.mixer.Sound('sound/thunder.mp3').stop()

    def Enter(self, params=None):
        self.rain.play(-1)
        pygame.mixer.Sound('sound/thunder.mp3').play()

    def render(self, screen):
    # Clear screen and draw raindrops
        if not self.mainScreen:
            screen.fill(BLACK)
            if 50 <= self.introTimer <= 53:
                screen.blit(pygame.image.load('graphics/lightning.png'), (WIDTH // 6, 0))
                self.lightning_active = True
                self.lightning_flash_count = random.randint(2, 5)
                self.lightning_alpha = 255 
            elif self.introTimer > 53:
                if self.lightning_active and self.lightning_flash_count > 0:
                    lightning_surface = pygame.Surface((WIDTH, HEIGHT))
                    lightning_surface.set_alpha(self.lightning_alpha)
                    lightning_surface.fill(WHITE)
                    screen.blit(lightning_surface, (0, 0))

        if self.mainScreen:
            screen.blit(pygame.image.load('graphics/intro.jpeg'), (0, 0))
            for drop in self.raindrops:
                drop.draw(screen)

            # Apply lightning effect with fade-out
            if self.lightning_active and self.lightning_flash_count > 0:
                lightning_surface = pygame.Surface((WIDTH, HEIGHT))
                lightning_surface.set_alpha(self.lightning_alpha)
                lightning_surface.fill(WHITE)
                screen.blit(lightning_surface, (0, 0))

            # Title with Outline
            title_text = "GHOST ARENA"
            t_title_color = (139, 0, 0)
            title_font = gameFont['large']
            
            # Render the title outline in red and black
            # outline_offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2)]  # Positions for red outline
            # for offset in outline_offsets:
            #     outline_surface = title_font.render(title_text, True, (255, 0, 0))
            #     outline_rect = outline_surface.get_rect(center=(WIDTH / 2 + offset[0], HEIGHT / 3 + offset[1]))
            #     screen.blit(outline_surface, outline_rect)

            black_offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Positions for black outline
            for offset in black_offsets:
                outline_surface = title_font.render(title_text, True, (199, 199, 209))
                outline_rect = outline_surface.get_rect(center=(WIDTH / 2 + offset[0], HEIGHT / 3 + offset[1]))
                screen.blit(outline_surface, outline_rect)

            # Render the main title text in white
            title_surface = title_font.render(title_text, True, t_title_color)
            title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3))
            screen.blit(title_surface, title_rect)

            # Start Option with Outline
            t_start_color = (55, 0, 0) 
            start_text = "START"
            option_font = gameFont['medium']
            y_pos = HEIGHT / 2 + 210

            # Render the "START" option outline in red and black
            # for offset in outline_offsets:
            #     outline_surface = option_font.render(start_text, True, (255, 0, 0))
            #     outline_rect = outline_surface.get_rect(center=(WIDTH / 2 + offset[0], y_pos + offset[1]))
            #     screen.blit(outline_surface, outline_rect)

            for offset in black_offsets:
                outline_surface = option_font.render(start_text, True, (199, 199, 209))
                outline_rect = outline_surface.get_rect(center=(WIDTH / 2 + offset[0], y_pos + offset[1]))
                screen.blit(outline_surface, outline_rect)

            # Render the main "START" text
            option_surface = option_font.render(start_text, True, t_start_color)
            option_rect = option_surface.get_rect(center=(WIDTH / 2, y_pos))
            screen.blit(option_surface, option_rect)

            t_start_color = (55, 0, 0) 
            start_text = "Press SPACE to skip intro"
            option_font = gameFont['medium']
            y_pos = HEIGHT / 2 + 300

            # Render the "START" option outline in red and black
            # for offset in outline_offsets:
            #     outline_surface = option_font.render(start_text, True, (255, 0, 0))
            #     outline_rect = outline_surface.get_rect(center=(WIDTH / 2 + offset[0], y_pos + offset[1]))
            #     screen.blit(outline_surface, outline_rect)

            for offset in black_offsets:
                outline_surface = option_font.render(start_text, True, (199, 199, 209))
                outline_rect = outline_surface.get_rect(center=(WIDTH / 2 + offset[0], y_pos + offset[1]))
                screen.blit(outline_surface, outline_rect)

            # Render the main "START" text
            option_surface = option_font.render(start_text, True, t_start_color)
            option_rect = option_surface.get_rect(center=(WIDTH / 2, y_pos))
            screen.blit(option_surface, option_rect)

    def update(self, dt, events):
        if not self.mainScreen:
            self.introTimer += 1
            print(self.introTimer)
        for event in events:
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                sound = pygame.mixer.Sound('sound/hit.wav')
                sound.play()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if self.option == 1:
                        self.option = 2
                    else:
                        self.option = 1
                    self.showNum = False
                if event.key == pygame.K_RETURN:
                    self.showNum = True
                    stateManager.Change('tutorial', {})
                if event.key == pygame.K_SPACE:
                    stateManager.Change('lobby', {})

        # Update raindrops
        for drop in self.raindrops:
            drop.fall()

        # Handle lightning effect with fading
        if self.lightning_active:
            
            if self.lightning_flash_count > 0:
                # Start with a bright flash and fade out
                self.lightning_alpha -= 25  # Decrease alpha to create fade-out effect
                if self.lightning_alpha <= 0:
                    # Reset for next flash in sequence
                    self.lightning_flash_count -= 1
                    if self.lightning_flash_count <= 1:
                        self.mainScreen = True
                    self.lightning_alpha = 255  # Reset alpha for the next flash
                    self.lightning_timer = 0  # Reset timer between flashes
            else:
                # End the lightning effect after all flashes in the sequence
                self.lightning_active = False
                
                self.lightning_alpha = 255
                self.lightning_timer = 0
                # Set a new random interval before the next lightning strike
                self.lightning_cooldown = random.randint(200, 500)

        else:
            # Countdown to the next lightning strike
            self.lightning_timer += 1
            if self.lightning_timer >= self.lightning_cooldown:
                # Start a new lightning sequence
                self.lightning_active = True
                pygame.mixer.Sound('sound/thunder.mp3').play()
                self.lightning_flash_count = random.randint(2, 5)  # Random number of flashes per strike
                self.lightning_alpha = 255  # Start with full brightness for each strike
                self.lightning_timer = 0