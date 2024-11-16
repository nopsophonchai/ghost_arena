from src.states.BaseState import BaseState
import pygame, sys
from ..Dependency import *

class TutorialState(BaseState):
    def __init__(self):
        super(TutorialState, self).__init__()
        self.step = 0
        self.bg_image = pygame.image.load("./graphics/bgtwo.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 5, HEIGHT + 5))

        self.instructions = [
            "Welcome to the Ghost Arena! Use the arrow keys to select the options.",
            "Press 'Enter' to attack enemies and confirm your selection. Attacks are made with cards.",
            "Each card represents a spell or an item attack you can use.",
            "At the start of each round, draw 4 cards to your hand.",
            "When you use a card, it goes to the bottom of the deck.",
            "This is a turn-based game. You can only target one enemy per turn.",
            "Press 0 for special interactions any page"
        ]

        # Typing effect variables
        self.current_instruction = ""
        self.current_char_index = 0
        self.typing_speed = 0.005  # Adjust typing speed as needed
        self.time_since_last_char = 0
        self.show_next_button = False

        # Button to advance the tutorial
        self.next_button = pygame.Rect(1150, 620, 100, 50)

    def Enter(self, params):
        self.step = 0
        self.start_typing_effect()

    def Exit(self):
        pass

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))

        t_title = gameFont['large'].render("How to Play", False, (139, 0, 0))
        rect = t_title.get_rect(center=(WIDTH / 2, HEIGHT / 3 - 140))
        screen.blit(t_title, rect)

        # Display the instruction text with a typing effect
        text_surface = gameFont['small'].render(self.current_instruction, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text_surface, text_rect)

        # Show "Next" button if line is fully displayed
        if self.show_next_button:
            pygame.draw.rect(screen, (137, 148, 153), self.next_button)
            next_text = gameFont['small'].render("Next", True, (0, 0, 0))
            screen.blit(next_text, (self.next_button.x + 20, self.next_button.y + 10))

    def update(self, dt, events):
        self.time_since_last_char += dt
        if self.time_since_last_char >= self.typing_speed:
            # Add one character at a time to current instruction
            if self.current_char_index < len(self.instructions[self.step]):
                self.current_instruction += self.instructions[self.step][self.current_char_index]
                self.current_char_index += 1
                self.time_since_last_char = 0
            else:
                # Instruction fully displayed, show next button
                self.show_next_button = True

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.show_next_button:
                    self.next_step()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                     stateManager.Change('story', {})

    def next_step(self):
        self.step += 1
        if self.step < len(self.instructions):
            # Move to the next instruction and reset the typing effect
            self.start_typing_effect()
        else:
            # End of tutorial, transition to the next state
            stateManager.Change('story', {})

    def start_typing_effect(self):
        """Initialize typing effect for the current instruction."""
        self.current_instruction = ""
        self.current_char_index = 0
        self.time_since_last_char = 0
        self.show_next_button = False
