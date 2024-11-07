import traceback
from src.Items.Item import Item

class Weapon(Item):
    def __init__(self,name, damage,weaponType, effects = None,beyond = False):
        super().__init__(name)
        self.damage = damage
        self.type = 'Weapon'
        self.weaponType = weaponType
        self.effects = effects or []
        self.beyond = beyond
        self.timer = 0

    def attack(self,target):
        if target:
            # print(target)
            if not self.beyond:
                target.damageEnemy(self.damage)
                self.applyEffect(target)
            else:
                target.damageEnemy(self.damage)
                self.applyEffect(target)

    def applyEffect(self,target):
        if target:
            for effect in self.effects:
                effect[0](target, self.damage)

