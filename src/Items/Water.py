import traceback
from src.Items.Item import Item
from src.Items.StatusEffect import StatusEffect
import math

class Water(Item):
    def __init__(self,name, damage,spellType):
        super().__init__(name)
        self.damage = damage
        self.type = 'Spell'
        self.weaponType = 'range'
        self.damageType = 'Water'
        self.interfaceFlag = False
        self.spellList = [('Splash',self.splash),('Water of Life',self.waterOfLife),('Tsunami',self.tsunami)]
        self.effects = []
        self.playerEffects = []


    def attack(self,target,player,selected):
        self.interfaceFlag = True
        chosenSpell = self.spellList[selected][1]
        chosenSpell(target,player)

    def splash(self,target,player):
        if target:
            target.damageEnemy(self.damage,self.damageType)
            target.damage -= 1
    
    def waterOfLife(self,target,player):
        if player:
            player.health += math.ceil(self.damage*1.5)
    
    def tsunami(self,target,player):
        if self.useThree < 1:
            if target:
                target.health = player.health 
                target.damageEnemy(self.damage)
                self.useThree += 1
                print('TSUNAMI')
        else:
            target.damageEnemy(1)

    def getCombinedEffects(self):
        return self.effects + self.playerEffects