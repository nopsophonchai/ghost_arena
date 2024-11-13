from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *
from src.resources import *
pygame.font.init()
gameFont = {
        'small': pygame.font.Font('./fonts/font.ttf', 24),
        'medium': pygame.font.Font('./fonts/font.ttf', 48),
        'large': pygame.font.Font('./fonts/font.ttf', 96)
}
class GameOver(BaseState):
    def __init__(self):
        super(GameOver, self).__init__()
        #start = 1,       ranking = 2
        self.option = 1
        self.showNum = False

    def Exit(self):
        pass

    def Enter(self, params):
        stateManager.Reset()


    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()         
                if event.key == pygame.K_RETURN:
                  stateManager.Change('start',{})


    def render(self, screen):
        # title
        t_title = gameFont['large'].render("Game Over!", False, (255, 255, 255))
        rect = t_title.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(t_title, rect)
        t_title = gameFont['medium'].render("Press Enter to Restart!", False, (255, 255, 255))
        rect = t_title.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(t_title, rect)
