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
        'mediumsmall': pygame.font.Font('./fonts/font.ttf', 30),

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
        'GongGoiIdle': sprite_collection['GG_Green_Idle'].animation,
        'GongGoiHurt': sprite_collection['GG_Green_Hurt'].animation,
        'GG_PurpleIdle': sprite_collection['GG_Purple_Idle'].animation,
        'GG_YellowIdle': sprite_collection['GG_Yellow_Idle'].animation,
        'GG_GreenHurt': sprite_collection['GG_Green_Hurt'].animation,
        'GG_RedHurt': sprite_collection['GG_Red_Hurt'].animation,
        'GG_PurpleHurt': sprite_collection['GG_Purple_Hurt'].animation,
        'GG_YellowHurt': sprite_collection['GG_Yellow_Hurt'].animation,
        'MaeNakIdle': sprite_collection['MaeNak_Idle'].animation,
        'MaeNakHurt': sprite_collection['MaeNak_Hurt'].animation,
        'KaIdle': sprite_collection['Ka_Idle'].animation,
        'KaHurt': sprite_collection['Ka_Hurt'].animation,
        'KrasueIdle': sprite_collection['KraSue_Idle'].animation,
        'KrasueHurt': sprite_collection['KraSue_Hurt'].animation,
        'KrasueIdle': sprite_collection['KraSue_Idle'].animation,
        'KasueHurt': sprite_collection['KraSue_Hurt'].animation,
        'DangIdle': sprite_collection['MaeNakDaeng_Idle'].animation,
        'DangHurt': sprite_collection['MaeNakDaeng_Hurt'].animation,
        'NangRamIdle': sprite_collection['NangRam_Idle'].animation,
        'NangRamHurt': sprite_collection['NangRam_Hurt'].animation,
        'PhraiIdle': sprite_collection['Prai_Idle'].animation,
        'PhraiHurt': sprite_collection['Prai_Hurt'].animation,
        'MonkIdle': sprite_collection['Monk_Idle'].animation,
        'MonkHurt': sprite_collection['Monk_Hurt'].animation,
        'FakerIdle': sprite_collection['Faker_Idle'].animation,
        'FakerHurt': sprite_collection['Faker_Hurt'].animation,



        
        
}
