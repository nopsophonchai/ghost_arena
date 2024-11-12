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

        self.bg_music = pygame.mixer.Sound('sound/music.mp3')

        stateManager.SetScreen(self.screen)

        # Define states including StartState
        states = {
            'start': StartState(),
            'play': Play(),
            'save': SaveSelect(),
            'tutorial': TutorialState(),
            'story': StoryState(),
            'select': EnemySelection(),
            'gameover': GameOver(),
            'lobby': Lobby(),
            'character': Character(),
            'shop': Shop()
        }
        stateManager.SetStates(states)

    def RenderBackground(self):
        self.screen.fill((0, 0, 0))

    def play_intro_video(self, video_path):
        """ Plays the intro video, then releases resources and switches to 'start' state """
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  
            frame = cv2.resize(frame, (self.screen.get_width(), self.screen.get_height()))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
            self.screen.blit(frame_surface, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.time.Clock().tick(90)  # Adjust to control playback speed

        cap.release()  # Release video resources
        print("Intro video finished, transitioning to StartState.")
        stateManager.Change('start', {})  # Transition to StartState

    def PlayGame(self):
        """ Main game loop with intro video and state transitions """
        # Play the main intro video before starting the main loop
        self.play_intro_video("./video/first-intro.mp4")

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


if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()
