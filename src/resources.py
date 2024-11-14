from src.StateMachine import StateMachine       
from src.resources import *
from src.Util import *
import pygame
import json

pygame.font.init()
stateManager = StateMachine()
message = "Resource"
gameFont = {
        'small': pygame.font.Font('./fonts/font.ttf', 24),
        'medium': pygame.font.Font('./fonts/font.ttf', 48),
        'large': pygame.font.Font('./fonts/font.ttf', 96)
}




sprite_collection = SpriteManager().spriteCollection



aniList = {
    'playerIdle': sprite_collection['Player_Idle'].animation,
    'playerHurt': sprite_collection['Player_Hurt'].animation
}

enemyAni = {
        'PretaIdle': sprite_collection['Preta_Idle'].animation,
        'PretaHurt': sprite_collection['Preta_Hurt'].animation,
        
}
