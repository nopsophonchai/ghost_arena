# from src.constants import *
# from src.recourses import *
class EntityConf:
    def __init__(self, cards, health, damage):
        self.cards = cards
        self.health = health
        self.damage = damage
        
         


 = {
    'player': EntityConf(animation=gPlayer_animation_list, walk_speed=PLAYER_WALK_SPEED,
                         x=WIDTH/2-24, y=HEIGHT/2 -33, width=48, height=66,
                         health=6, offset_x=0, offset_y=15),
    'skeleton':EntityConf(animation=gSkeleton_animation_list, width=48, height=48, health=2)
}