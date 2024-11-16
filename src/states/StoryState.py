from src.states.BaseState import BaseState
import pygame, sys
from ..Dependency import *
from src.Player import Player

class StoryState(BaseState):
    def __init__(self):
        super(StoryState, self).__init__()
        self.story_text = [
            "The Demon King of the shadowed realms has torn your soul from its sanctuary.",
            "To reclaim what is yours, you must confront him and his legion of spectral minions.",
            "The battle will take place on desecrated grounds where light has long faded.",
            "Only the strongest can hope to reunite with their lost soul."
        ]
        self.current_line_index = 0
        self.current_line = ""
        self.current_char_index = 0
        self.typing_speed = 0.025  # Adjust typing speed as needed
        self.time_since_last_char = 0
        self.show_next_button = False
        self.player = Player()
        self.show_start_button = False

        # Background
        self.bg_image = pygame.image.load("./graphics/bgtwo.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 5, HEIGHT + 5))

        # Button to advance the story
        self.next_button = pygame.Rect(1150, 620, 100, 50)

    def Enter(self, params):
        self.current_line_index = 0
        self.current_line = ""
        self.current_char_index = 0
        self.time_since_last_char = 0
        self.show_next_button = False
        self.show_start_button = False

    def Exit(self):
        pass

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))

        # Render the "Story" title
        t_title = gameFont['large'].render("Story", False, (139, 0, 0))
        rect = t_title.get_rect(center=(WIDTH / 2, HEIGHT / 3 - 140))
        screen.blit(t_title, rect)

        # Display the text with a typing effect
        text_surface = gameFont['small'].render(self.current_line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text_surface, text_rect)

        # Show "Next" button if line is fully displayed
        if self.show_next_button:
            pygame.draw.rect(screen, (137, 148, 153), self.next_button)
            next_text = gameFont['small'].render("Next", True, (0, 0, 0))
            screen.blit(next_text, (self.next_button.x + 20, self.next_button.y + 10))
        if self.show_start_button:
            
            pygame.draw.rect(screen, (137, 148, 153), self.next_button)
            next_text = gameFont['small'].render("Start", True, (0, 0, 0))
            screen.blit(next_text, (self.next_button.x + 20, self.next_button.y + 10))    

    def update(self, dt, events):
        self.time_since_last_char += dt
        if self.time_since_last_char >= self.typing_speed:
            # Add one character at a time to current line
            if self.current_char_index < len(self.story_text[self.current_line_index]):
                self.current_line += self.story_text[self.current_line_index][self.current_char_index]
                self.current_char_index += 1
                self.time_since_last_char = 0
            else:
                # Line fully displayed, show next button
                self.show_next_button = True

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.show_next_button:
                    self.next_line()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    stateManager.Change('lobby',{'player': self.player})

    def next_line(self):
        self.current_line_index += 1
        if self.current_line_index < len(self.story_text):
            # Move to the next line and reset the typing effect
            self.current_line = ""
            self.current_char_index = 0
            self.show_next_button = False
            self.show_start_button = True
        else:
            # End of story, transition to the next state
            stateManager.Change('lobby',{'player': self.player})
