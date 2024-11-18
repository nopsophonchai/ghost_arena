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
        'super_small': pygame.font.Font('./fonts/font.ttf', 20),
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
        self.healthPrice = 4
        self.damagePrice = 4
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

        self.bottom_image = pygame.image.load("./graphics/lotus_monk.png")

        self.image3 = pygame.image.load('graphics/skeleton_point_left.png')
        self.image3 = pygame.transform.scale(self.image3,(70,70))

        self.monk_idle_animation = sprite_collection['Monk_Idle'].animation
    

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




    def Exit(self):
        print(self.weaponSelect)
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
        scaled_bottom_image = pygame.transform.scale(self.bottom_image, (270, 200))
        screen.blit(scaled_bottom_image,(WIDTH/2 - 350,HEIGHT/4 - 20))
        screen.blit(scaled_bottom_image,(WIDTH/2 + 70,HEIGHT/4 - 20))
        screen.blit(scaled_bottom_image,(WIDTH/4 - 135,HEIGHT/2 - 70))
        screen.blit(scaled_bottom_image,(WIDTH/2 + 170,HEIGHT/2 - 70))
        screen.blit(scaled_bottom_image,(WIDTH/4 - 170,HEIGHT/2 + 70))
        screen.blit(scaled_bottom_image,(WIDTH/2 + 210,HEIGHT/2 + 70))
        screen.blit(scaled_bottom_image,(WIDTH/2 - 150 ,HEIGHT/4 - 120))
        # Scale up the monk
        scale_factor = 2.5  
        monk_scaled = pygame.transform.scale(
            self.monk_idle_animation.image, 
            (
                int(self.monk_idle_animation.image.get_width() * scale_factor),
                int(self.monk_idle_animation.image.get_height() * scale_factor)
            )
        )
        screen.blit(monk_scaled, (WIDTH / 2 - monk_scaled.get_width() / 2, HEIGHT / 2 - monk_scaled.get_height() / 2))
                
        if not self.weaponSelect:
            locations = [(WIDTH / 3, HEIGHT / 3),(WIDTH / 1.5, HEIGHT / 3),(WIDTH / 3 - 100, HEIGHT / 2), (WIDTH / 1.5 + 100, HEIGHT / 2), (WIDTH / 3 - 150, HEIGHT / 1.5),(WIDTH / 1.5 + 120, HEIGHT / 1.5)]
            priceLocations = [(WIDTH / 3, HEIGHT / 2.6),(WIDTH / 1.5, HEIGHT / 2.65),(WIDTH / 3 - 100, HEIGHT / 1.8), (WIDTH / 1.5 + 100, HEIGHT / 1.8)]
            item_spacing = 200
            total_width = item_spacing * (4)
            start_x = (WIDTH - total_width + 200) / 2
            #bg_color = (0, 0, 0)
            padding = 5
            text_surface = gameFont['super_small'].render(f'Back To Lobby', True, (255, 255, 255))
            #bg_surface = pygame.Surface((text_surface.get_width() + 2 * padding, text_surface.get_height() + 2 * padding))
            #bg_surface.fill(bg_color)
            rect = text_surface.get_rect(center=(WIDTH / 4 - 80, HEIGHT / 4 + 480))
            #bg_rect = bg_surface.get_rect(center=rect.center)
            #screen.blit(bg_surface, bg_rect)
            if self.select == 6:
                
                pygame.draw.rect(screen, (166, 218, 149), rect.inflate(20, 10))
            screen.blit(text_surface, rect)
            for i in range(4):
                text_surface = gameFont['small'].render(f'{self.chosenList[i][1]}', True, (0, 0, 0))
                rect = text_surface.get_rect(center=locations[i])
                if self.select == i:
                    pygame.draw.circle(screen, (255,255,194), rect.center, max(100, 100) // 2 + 10, 3)
                    pygame.draw.circle(screen, (255,232,124), rect.center, max(120, 120) // 2 + 10, 3)
                    pygame.draw.circle(screen, (255,216,1), rect.center, max(150, 150) // 2 + 10, 3)
                    pygame.draw.rect(screen, (166, 218, 149), rect.inflate(20, 10))
                screen.blit(text_surface, rect)
                text_surface = gameFont['small'].render(f'{self.chosenList[i][2]}', True, (255, 215, 0))
                rect = text_surface.get_rect(center=priceLocations[i])
                if self.select == i:
                    
                    pygame.draw.rect(screen, (166, 218, 149), rect.inflate(20, 10))
                screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Increase health by 2', True, (0, 0, 0))
            rect = text_surface.get_rect(center=(WIDTH / 4 - 30, HEIGHT /2 + 150 ))
            if self.select == 4:
                if self.healthBought < 11:
                    pygame.draw.circle(screen, (255,255,194), rect.center, max(100, 100) // 2 + 10, 3)
                    pygame.draw.circle(screen, (255,232,124), rect.center, max(120, 120) // 2 + 10, 3)
                    pygame.draw.circle(screen, (255,216,1), rect.center, max(150, 150) // 2 + 10, 3)
                    pygame.draw.rect(screen, (166, 218, 149), rect.inflate(20, 10))
                else:
                    pygame.draw.rect(screen, (255, 255, 0), rect.inflate(20, 10))
            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'{self.healthPrice}', True, (255, 215, 0))
            rect = text_surface.get_rect(center=(WIDTH / 4 - 30, HEIGHT /2 + 180 ))
            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Increase damage by 1', True, (0, 0, 0))
            rect = text_surface.get_rect(center=(WIDTH / 2 + 350, HEIGHT /2 + 150 ))
            if self.select == 5:
                if self.damageBought < 11:
                    pygame.draw.circle(screen, (255,255,194), rect.center, max(100, 100) // 2 + 10, 3)
                    pygame.draw.circle(screen, (255,232,124), rect.center, max(120, 120) // 2 + 10, 3)
                    pygame.draw.circle(screen, (255,216,1), rect.center, max(150, 150) // 2 + 10, 3)
                    pygame.draw.rect(screen, (166, 218, 149), rect.inflate(20, 10))
                else:
                    pygame.draw.rect(screen, (255, 255, 0), rect.inflate(20, 10))
            
            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'{self.damagePrice}', True, (255, 215, 0))
            rect = text_surface.get_rect(center=(WIDTH / 2 + 350, HEIGHT /2 + 180 ))
            screen.blit(text_surface, rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Gold: {self.player.gold}', True, (255, 215, 0))
            rect = text_surface.get_rect(center=(150,65))
            screen.blit(text_surface,rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Damage: {self.player.damage}', True, (245, 64, 41))
            rect = text_surface.get_rect(center=(150,90))
            screen.blit(text_surface,rect)

            screen.blit(text_surface, rect)
            text_surface = gameFont['small'].render(f'Health: {self.player.maxHealth}', True, (105, 190, 40))
            rect = text_surface.get_rect(center=(150,120))
            screen.blit(text_surface,rect)

            # screen.blit(text_surface, rect)
            # text_surface = gameFont['small'].render(f'Health Price: {self.healthPrice}', True, (105, 190, 40))
            # rect = text_surface.get_rect(center=(630,150))
            # screen.blit(text_surface,rect)

        if self.weaponSelect:
            item_spacing = 200
            total_width = item_spacing * (len(self.weaponDict) - 1)
            start_x = (WIDTH - total_width) / 2
            text_surface = gameFont['medium'].render('Which item do you want to enchant?', True, (255, 255, 255))
            rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 6))
            screen.blit(text_surface, rect)

            for i, (key, weapon) in enumerate(self.weaponDict.items()):
                padding = 15
                bg_color = (125, 125, 125)
                text_surface = gameFont['small'].render(weapon.name, True, (255, 255, 255))
                rect = text_surface.get_rect(center=(start_x + item_spacing * i, HEIGHT / 1.25))
                bg_surface = pygame.Surface((text_surface.get_width() + 2 * padding, text_surface.get_height() + 2 * padding))
                bg_surface.fill(bg_color)
                bg_rect = bg_surface.get_rect(center=rect.center)
                screen.blit(bg_surface, bg_rect)

                if self.select == i:
                    pygame.draw.rect(screen, (255, 0, 0), bg_rect.inflate(8, 8), 4)
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

        screen.blit(self.image3, (WIDTH / 8 - 80, HEIGHT / 4 + 435)) 

        

