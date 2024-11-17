import pygame, math, os
from pygame import mixer
import cv2
import numpy as np
from src.Dependency import *

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

music_channel = mixer.Channel(0)

music_channel.set_volume(0.2)

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ghost Arena")

        self.bg_music = pygame.mixer.Sound('sound/zelda.mp3')

        stateManager.SetScreen(self.screen)

        states = {
            'start': StartState(),
            'play': Play(),
            #'save': SaveSelect(),
            'tutorial': TutorialState(),
            'story': StoryState(),
            'select': EnemySelection(),
            'gameover': GameOver(),
            'lobby': Lobby(),
            'character': Character(),
            'shop': Shop()
        }
        stateManager.SetStates(states)
        stateManager.Change('start', {})

    def RenderBackground(self):
        self.screen.fill((0, 0, 0))

    

    def PlayGame(self):

        clock = pygame.time.Clock()

        while True:
            pygame.display.set_caption("Ghost Arena running with {:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            # Input handling
            events = pygame.event.get()

            # Update state
            stateManager.update(dt, events)

            # Render background and state
            self.RenderBackground()
            stateManager.render()
            

            # Screen update
            pygame.display.update()
            # print(sprite_collection)

if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()
