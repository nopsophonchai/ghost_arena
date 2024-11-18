import traceback
from src.Items.Item import Item
import pygame
from src.resources import *

class Weapon(Item):
    def __init__(self,name, damage,weaponType, effects = None,playerEffects = []):
        super().__init__(name)
        self.damage = damage
        self.type = 'Weapon'
        self.weaponType = weaponType
        self.effects = effects or []
        self.playerEffects = playerEffects or []
        self.beyond = False
        self.bungieGum = False
        self.timer = 0


    def attack(self,target):
        if target:
            print(self.damage)
            target.damageEnemy(self.damage)
            # target.addEffect(f'{self.name} used {chosenAttack[1]}!', (WIDTH / 3, HEIGHT / 6), duration=100)
            self.applyEffect(target)
            if self.beyond:
                target.damageEnemy(self.damage)
                self.applyEffect(target)


    def applyEffect(self,target):
        if target:
            for effect in self.effects:
                effect[0](target, self.damage)

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

        if len(self.getCombinedEffects()) > 0:
            effect_y_position = 65
            effect_y_positionTwo = 10
            # Loop through the first 3 effects (or fewer if there are less than 3)
            for i in range(min(3, len(self.getCombinedEffects()))):
                # Render the effect's name
                text_surface = pygame.font.Font('./fonts/font.ttf', 12).render(f"{self.getCombinedEffects()[i][1]}", True, (0, 0, 0))
                rect = text_surface.get_rect(center=(cardX + 260, cardY + effect_y_position))
                screen.blit(text_surface, rect)
                
                # Move down slightly after the effect's name
                effect_y_position += 10  # Adjust spacing as needed
                effect_y_positionTwo = 0
                # Split the effect's description by newline and render each line
                description_lines = self.getCombinedEffects()[i][2].split('\n')
                for line in description_lines:
                    # Render each line of the description
                    text_surface = pygame.font.Font('./fonts/font.ttf', 12).render(line, True, (0, 0, 0))
                    rect = text_surface.get_rect(center=(cardX + 260, cardY + effect_y_position + effect_y_positionTwo))
                    screen.blit(text_surface, rect)
                    # Move down for the next line in the description
                    effect_y_positionTwo += 10  # Adjust line spacing as necessary
                
                # Move down for the next effect
                effect_y_position += 60  # Adjust spacing between effects as necessary
