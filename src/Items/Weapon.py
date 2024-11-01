
from src.Items.Item import Item

class Weapon(Item):
    def __init__(self,name, damage,weaponType, effects = None):
        super().__init__(name)
        self.damage = damage
        self.type = 'Weapon'
        self.weaponType = weaponType
        self.effects = effects or []

    def attack(self,target):
        if target:
            # print(target)
            target.damageEnemy(self.damage)
    
    def applyEffect(self,target):
        if target:
            for effect in self.effects:
                effect(target)