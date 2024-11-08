import traceback
from src.Items.Item import Item

class Weapon(Item):
    def __init__(self,name, damage,weaponType, effects = None,playerEffects = []):
        super().__init__(name)
        self.damage = damage
        self.type = 'Weapon'
        self.weaponType = weaponType
        self.effects = effects or []
        self.playerEffects = playerEffects or []
        self.beyond = False
        self.timer = 0

    def attack(self,target):
        if target:
            target.damageEnemy(self.damage)
            self.applyEffect(target)
            if self.beyond:
                target.damageEnemy(self.damage)
                self.applyEffect(target)

    def applyEffect(self,target):
        if target:
            for effect in self.effects:
                effect[0](target, self.damage)



