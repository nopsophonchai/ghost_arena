from src.Enemies.Enemy import Enemy
from src.Items.StatusEffect import StatusEffect
import math

class Monk(Enemy):
    def __init__(self,name,health,damage,armor = 0):
        super().__init__(health,damage,armor,name='Monk',immune=[],weakness=[])
        self.attacks = {'normal':[self.exorcise],'dot':[self.heal]}
        self.gold = 4
    def exorcise(self,target):
        if target.health < 5:
            target.damageEnemy(self.damage, 'true')
        else:
            target.health = target.health // 2
        print(f'Monk exorcise!')

    def heal(self,target):
        self.health += int(target.health // 1.5)
        print(f'Monk Healed!')