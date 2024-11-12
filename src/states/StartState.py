from src.states.BaseState import BaseState
import pygame
import sys
from moviepy.editor import VideoFileClip
from ..Dependency import *

class StartState(BaseState):
    def __init__(self):
        super(StartState, self).__init__()

        # Load videos using moviepy
        self.intro_video = VideoFileClip('./video/secondd-intro.mp4')
        self.loop_video = VideoFileClip('./video/loopbg.mp4')
        self.current_video = self.intro_video  # Start with the intro video
        self.frame_iterator = None  # Iterator for extracting frames

        # State variables for text display
        self.option = 0
        self.showNum = False

    def Exit(self):
        # Close resources in moviepy if necessary
        if self.current_video:
            self.current_video.close()
        print("Resources released, exiting StartState.")

    def Enter(self, params=None):
        # Start with the intro video and prepare the frame iterator
        self.current_video = self.intro_video
        print("Entered StartState, ready to play intro video.")
        self.frame_iterator = self.current_video.iter_frames(fps=24, dtype="uint8")

    def render(self, screen):
        # Get the next frame from the iterator and resize it to fit the screen
        try:
            frame = next(self.frame_iterator)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame_surface = pygame.transform.scale(frame_surface, (screen.get_width(), screen.get_height()))
            screen.blit(frame_surface, (0, 0))
        except StopIteration:
            # If the intro video ends, switch to the loop video
            if self.current_video == self.intro_video:
                self.current_video = self.loop_video
                self.frame_iterator = self.current_video.iter_frames(fps=24, dtype="uint8")
                print("Switched to loop video.")
        except Exception as e:
            print("Error retrieving video frame:", e)
            screen.fill((0, 0, 0))  # Fallback to a black screen

        # Overlay text
        t_title = gameFont['large'].render("GHOST ARENA", False, (255, 255, 255))
        rect = t_title.get_rect(center=(screen.get_width() / 2, screen.get_height() / 3))
        screen.blit(t_title, rect)

        # Option colors
        t_start_color = (255, 255, 255)
        t_highscore_color = (255, 255, 255)

        if self.option == 1:
            t_start_color = (103, 255, 255)

        if self.option == 2:
            t_highscore_color = (103, 255, 255)

        # Display additional text
        if self.showNum:
            work = gameFont['small'].render("Yeah", False, t_start_color)
            screen.blit(work, (0, 0))

        t_start = gameFont['mediumsmall'].render("START", False, t_start_color)
        rect = t_start.get_rect(center=(screen.get_width() / 3, screen.get_height() / 2 + 120))
        screen.blit(t_start, rect)

        t_high = gameFont['mediumsmall'].render("Tutorial", False, t_highscore_color)
        rect = t_high.get_rect(center=(screen.get_width() / 2 + 130, screen.get_height() / 2 + 120))
        screen.blit(t_high, rect)

        pygame.display.flip()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.option = 2 if self.option == 1 else 1
                    self.showNum = False
                if event.key == pygame.K_RETURN:
                    if self.option == 1:
                        stateManager.Change('save', {})
                    elif self.option == 2:
                        stateManager.Change('tutorial', {})  
                        self.showNum = True
