import traceback
from src.Items.Item import Item
from src.Items.StatusEffect import StatusEffect

class Fire(Item):
    def __init__(self,name, damage,spellType):
        super().__init__(name)
        self.damage = damage
        self.type = 'Spell'
        self.weaponType = 'range'
        self.damageType = 'Fire'
        self.interfaceFlag = False
        self.spellList = [('Burning',self.burning),('Healing Flame',self.healingFlame),('Magma',self.magma)]
        self.effects = []
        self.playerEffects = []


    def attack(self,target,player,selected):
        self.interfaceFlag = True
        chosenSpell = self.spellList[selected][1]
        chosenSpell(target,player)

    def burning(self,target,player):
        if target:
            target.damageEnemy(self.damage,self.damageType)
            burn = StatusEffect('burn',self.damage//2,2,self.damageType)
            target.statusEffects.append(burn)
    
    def healingFlame(self,target,player):
        if player:
            player.health += self.damage
    
    def magma(self,target,player):
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