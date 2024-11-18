from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *
from src.resources import *
from src.Player import Player
from src.Enemies.GongGoi import GongGoi
from src.Enemies.Preta import Preta
from src.Items.Weapon import Weapon
from src.Items.effects import gameEffects,playerEffects
from src.Enemies.Monk import Monk
pygame.font.init()
import random as rd

gameFont = {
        'small': pygame.font.Font('./fonts/font.ttf', 24),
        'medium': pygame.font.Font('./fonts/font.ttf', 48),
        'large': pygame.font.Font('./fonts/font.ttf', 96)
}
class Shop(BaseState):
    def __init__(self):
        super(Shop, self).__init__()
        self.confirm = False
        self.select = 0
        self.chosen = 0

        self.healthBought = 0
        self.damageBought = 0
        self.healthPrice = 2
        self.damagePrice = 2
        self.price = 0

        self.weaponSelect = False
        self.chosenEffect = None

        self.alertTimer = 0
        self.alert = False

        self.free = False

        self.roundCount = 0
        self.thisRound = 0

        self.ibought = [0,0,0,0]

        self.background_image = pygame.transform.scale(pygame.image.load("./graphics/shop_background.png"), (WIDTH, HEIGHT))
        self.monk_idle_animation = sprite_collection['Monk_Idle'].animation
        self.bottom_image = pygame.image.load("./graphics/lotus_monk.png")


    def Reset(self):
        self.confirm = False
        self.select = 0
        self.chosen = 0

        self.healthBought = 0
        self.damageBought = 0
        self.healthPrice = 2
        self.damagePrice = 2
        self.price = 0

        self.weaponSelect = False
        self.chosenEffect = None

        self.alertTimer = 0
        self.alert = False

        self.free = False

        self.roundCount = 0
        self.thisRound = 0

        self.ibought = [0,0,0,0]
        self.enemy = Monk('Monk',80,10)



    def Exit(self):
        print(self.weaponSelect)
        self.player.refresh()
        self.select = 0
        self.weaponSelect = False

    def Enter(self, params):
        print(self.weaponSelect)
        
        self.weaponSelect = False
        if 'player' in params:
            self.player = params['player']
        if 'free' in params:
            self.free = params['free']
        if 'round' in params:
            self.round = params['round']
        if self.round != self.thisRound:
            self.roundCount = 0
        if self.roundCount == 0:
            self.thisRound = self.round
            self.ibought = [0,0,0,0]
            self.itemList = list(gameEffects.values())
            self.itemList.extend(list(playerEffects.values()))
            print()
            self.chosenList = rd.sample(self.itemList,4)
            self.weaponDict = {key: item for key, item in self.player.items.items() if item.type != 'Spell'}
            self.roundCount = 1

    def update(self, dt, events):
        self.monk_idle_animation.update(dt)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.weaponSelect:
                        self.select = (self.select - 1) % len(self.weaponDict)
                    else:
                        self.select = (self.select - 1) % 7
                elif event.key == pygame.K_RIGHT:
                    if self.weaponSelect:
                        self.select = (self.select + 1) % len(self.weaponDict)
                    else:
                        self.select = (self.select + 1) % 7
                elif event.key == pygame.K_0:
                    stateManager.Change('play',{'player': self.player,'enemy':Monk('Monk',(80),(10))})
                elif event.key == pygame.K_RETURN:
                    self.confirm = True  
        if self.confirm:
            self.process_confirm_action()

    def process_confirm_action(self):
        self.confirm = False 
        if self.weaponSelect:
            playerEffectName = [effect[1] for effect in list(self.player.items.items())[self.select][1].playerEffects] + [effect[1] for effect in list(self.player.items.items())[self.select][1].effects]
            if self.chosenEffect[1] in playerEffectName or len(list(self.player.items.items())[self.select][1].playerEffects) + len(list(self.player.items.items())[self.select][1].effects) > 2:
                print('Effect already exists!')
                self.alert = True

            elif self.chosenEffect[1] in [i[1] for i in list(playerEffects.values())]:
                match self.chosenEffect[1]:
                    case 'Beyond...':
                        list(self.player.items.items())[self.select][1].beyond = True
                    case 'Bungie Gum':
                        list(self.player.items.items())[self.select][1].bungieGum = True
                list(self.player.items.items())[self.select][1].playerEffects.append(self.chosenEffect)
                if not self.free:
                    self.player.gold -= self.price
                self.ibought[self.chosen] = 1
            else:
                list(self.player.items.items())[self.select][1].effects.append(self.chosenEffect)
                if not self.free:
                    self.player.gold -= self.price
                self.ibought[self.chosen] = 1
            self.weaponSelect = False
            self.price = 0

        else:
            if self.select == 6:
                stateManager.Change('lobby', {'player': self.player})
            elif self.select == 4:
                if self.player.gold >= self.healthPrice or self.free:
                    if self.free:
                        if self.healthBought >= 11 and self.player.gold >= self.healthPrice:
                            self.player.gold -= self.healthPrice
                            self.player.maxHealth += 2
                            self.healthPrice += 2 * self.healthBought
                            # self.player.playerScale(1)
                            self.healthBought += 1
                        elif self.healthBought < 11:
                            self.player.maxHealth += 2
                            self.healthPrice += 2 * self.healthBought
                            # self.player.playerScale(1)
                            self.healthBought += 1
                    else:
                        self.player.gold -= self.healthPrice
                        self.player.maxHealth += 2
                        self.healthPrice += 2 * self.healthBought
                        # self.player.playerScale(1)
                        # print(self.player.items['sword'].damage)
                        self.healthBought += 1
            elif self.select == 5:
                if self.player.gold >= self.damagePrice or self.free:
                    if self.free:
                        if self.damageBought >= 11 and self.player.gold >= self.damagePrice:
                            self.player.gold -= self.damagePrice
                            self.player.maxDamage += 1
                        elif self.damageBought < 11:
                            self.player.maxDamage += 1
                    else:
                        self.player.gold -= self.damagePrice
                        self.player.maxDamage += 1
                    self.damagePrice += 2 * self.damageBought
                    self.player.playerScale(1)
                    print(self.player.items['sword'].damage)
                    self.damageBought += 1
            elif self.select < 4:
                #print(self.chosenList)
                if (self.player.gold >= self.chosenList[self.select][2] or self.free )and self.ibought[self.select] == 0:
                    self.chosen = self.select
                    
                    self.weaponSelect = True
                    self.price = self.chosenList[self.select][2]
                    self.chosenEffect = (self.chosenList[self.select][0], self.chosenList[self.select][1],self.chosenList[self.select][3])
                    self.select = 0
                    #print(self.chosenEffect)


                

                    
    def render(self, screen):
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.bottom_image, ((WIDTH - self.bottom_image.get_width()) // 2, HEIGHT - self.bottom_image.get_height()))
        center = self.monk_idle_animation.image.get_rect(center=(WIDTH//2,HEIGHT//2))
        screen.blit(self.monk_idle_animation.image, center)
        if not self.weaponSelect:
            locations = [(WIDTH / 3, HEIGHT / 3),(WIDTH / 1.5, HEIGHT / 3),(WIDTH / 3, HEIGHT / 1.5), (WIDTH / 1.5, HEIGHT / 1.5), (WIDTH / 3, HEIGHT / 1.25),(WIDTH / 1.5, HEIGHT / 1.25)]
            priceLocations = [(WIDTH / 3, HEIGHT / 2.7),(WIDTH / 1.5, HEIGHT / 2.7),(WIDTH / 3, HEIGHT / 1.4), (WIDTH / 1.5, HEIGHT / 1.4)]
            item_spacing = 200
            total_width = item_spacing * (4)
            start_x = (WIDTH - total_width + 200) / 2
            text_surface = gameFont['small'].render(f'Back to fighting!', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            if self.select == 6:
                pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
            screen.blit(text_surface, rect)
            for i in range(4):
                text_surface = gameFont['small'].render(f'{self.chosenList[i][1]}', True, (255, 255, 255))
                rect = text_surface.get_rect(center=locations[i])
                if self.select == i:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                screen.blit(text_surface, rect)
                text_surface = gameFont['small'].render(f'{self.chosenList[i][2]}', True, (255, 255, 255))
                rect = text_surface.get_rect(center=priceLocations[i])
                if self.select == i:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Increase health by 2', True, (255, 255, 255))
            rect = text_surface.get_rect(center=locations[4])
            if self.select == 4:
                if self.healthBought < 11:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                else:
                    pygame.draw.rect(screen, (255, 255, 0), rect.inflate(20, 10))
            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Increase damage by 1', True, (255, 255, 255))
            rect = text_surface.get_rect(center=locations[5])
            if self.select == 5:
                if self.damageBought < 11:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                else:
                    pygame.draw.rect(screen, (255, 255, 0), rect.inflate(20, 10))
            
            screen.blit(text_surface, rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Gold: {self.player.gold}', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(325,95))
            screen.blit(text_surface,rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Damage: {self.player.maxDamage}', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(325,120))
            screen.blit(text_surface,rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Health: {self.player.maxHealth}', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(325,150))
            screen.blit(text_surface,rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Health Price: {self.healthPrice}', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(600,150))
            screen.blit(text_surface,rect)

        if self.weaponSelect:
            item_spacing = 200
            total_width = item_spacing * (len(self.weaponDict) - 1)
            start_x = (WIDTH - total_width) / 2
            text_surface = gameFont['small'].render(f'Which item do you want to enchant?', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3))
            screen.blit(text_surface, rect)
            for i in range(len(self.weaponDict)):
                text_surface = gameFont['small'].render(list(self.weaponDict.items())[i][1].name, True, (255, 255, 255))
                rect = text_surface.get_rect(center=(start_x + item_spacing * i, HEIGHT / 1.25))
                if self.select == i:
                    pygame.draw.rect(screen, (0, 128, 255), rect.inflate(20, 10))
                screen.blit(text_surface, rect)
        if self.alert:
            self.alertTimer += 1
            pygame.draw.rect(screen,(255, 102, 102),(WIDTH/2 - 350, HEIGHT/2 - 150, 700,300))
            message = "Weapon already enchanted!\nEnchant another weapon!"
            lines = message.split("\n")
            for i, line in enumerate(lines):
                text_surface = gameFont['medium'].render(line, True, (255, 255, 255))
                rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 30 + i * 40))  # Adjust vertical spacing with `i * 40`
                screen.blit(text_surface, rect)
            if self.alertTimer >= 100:
                self.alertTimer = 0
                self.alert = False

        

