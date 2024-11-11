import traceback
from src.Items.Item import Item
from src.Items.StatusEffect import StatusEffect
import random as rd

class Rice(Item):
    def __init__(self,name, damage,spellType):
        super().__init__(name)
        self.damage = damage
        self.type = 'Spell'
        self.weaponType = 'range'
        self.damageType = 'Rice'
        self.interfaceFlag = False
        self.spellList = [('Throw',self.throw),('Eat',self.eat),('Bin Tha Bat',self.binthabat)]
        self.effects = []
        self.playerEffects = []


    def attack(self,target,player,selected):
        self.interfaceFlag = True
        chosenSpell = self.spellList[selected][1]
        chosenSpell(target,player)

    def throw(self,target,player):
        if target:
            target.damageEnemy(self.damage,self.damageType)

    
    def eat(self,target,player):
        if player:
            player.health += self.damage // 2
    
    def binthabat(self,target,player):
        if target:
            prob = rd.random()
            if prob <= 0.2:
                target.damageEnemy(1000000,self.damageType)

    def getCombinedEffects(self):
        return self.effects + self.playerEffects