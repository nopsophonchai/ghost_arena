import traceback
from src.Items.Item import Item
from src.Items.StatusEffect import StatusEffect
import pygame
from src.resources import *

class Fire(Item):
    def __init__(self,name, damage,spellType):
        super().__init__(name)
        self.damage = damage
        self.type = 'Spell'
        self.weaponType = 'range'
        self.damageType = 'Fire'
        self.interfaceFlag = False
        self.spellList = [('Burning',self.burning,f'Deal {self.damage} fire damage\nBurn for {self.damage//2} \nfire damage for 1 turn'),('Healing Flame',self.healingFlame,f'Heal for {self.damage} health'),('Magma',self.magma,f'Remove enemy armor\nDeal {self.damage} fire damage\nBurn for {self.damage} for 1 turn')]
        self.effects = []
        self.playerEffects = []
        self.fire = False


    def attack(self,target,player,selected):
        self.interfaceFlag = True
        chosenSpell = self.spellList[selected][1]
        chosenSpell(target,player)

    def burning(self,target,player):
        if target:
            target.damageEnemy(self.damage,self.damageType)
            burn = StatusEffect('burn',self.damage//2,2,self.damageType)
            target.statusEffects.append(burn)
            self.fire = True

    
    def healingFlame(self,target,player):
        if player:
            player.health += self.damage
    
    def magma(self,target,player):
        self.fire = True
        if self.useThree < 1:
            if target:
                target.armor = 0
                burn = StatusEffect('burn',self.damage,2,self.damageType)
                target.statusEffects.append(burn)
                target.damageEnemy(self.damage)
                self.useThree += 1
        else:
            target.damageEnemy(1)

    def getCombinedEffects(self):
        return self.effects + self.playerEffects
    
    def render(self,screen,x,y):
        cardX = x
        cardY = y
        screen.blit(pygame.image.load(f'graphics/items.png/{self.name}.png'),(cardX,cardY,0,0))

        text_surface = gameFont['small'].render(f"{self.name}", True, (0, 0, 0))
        rect = text_surface.get_rect(center=(cardX + 90, cardY + 22))
        screen.blit(text_surface, rect)

        text_surface = pygame.font.Font('./fonts/font.ttf', 16).render(f"Damage:", True, (0, 0, 0))
        rect = text_surface.get_rect(center=(cardX + 260, cardY + 20))
        screen.blit(text_surface, rect)

        text_surface = pygame.font.Font('./fonts/font.ttf', 16).render(f"{self.damage}", True, (0, 0, 0))
        rect = text_surface.get_rect(center=(cardX + 260, cardY + 40))
        screen.blit(text_surface, rect)

        if len(self.spellList) > 0:
            effect_y_position = 65
            effect_y_positionTwo = 10
            for i in range(3):
                text_surface = pygame.font.Font('./fonts/font.ttf', 10).render(f"{self.spellList[i][0]}", True, (0, 0, 0))
                rect = text_surface.get_rect(center=(cardX + 260, cardY + effect_y_position))
                screen.blit(text_surface, rect)
                effect_y_position += 10 
                effect_y_positionTwo = 0
                description_lines = self.spellList[i][2].split('\n')
                for line in description_lines:
                    text_surface = pygame.font.Font('./fonts/font.ttf', 10).render(line, True, (0, 0, 0))
                    rect = text_surface.get_rect(center=(cardX + 260, cardY + effect_y_position + effect_y_positionTwo))
                    screen.blit(text_surface, rect)
                    effect_y_positionTwo += 10 
                effect_y_position += 60 
