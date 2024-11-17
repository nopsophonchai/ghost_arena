import random as rd
from src.Items.Debuff import Debuff
# def beyond(weapon):



def here_comes_the_sun(target,damage = 0):
    def apply(target):

        target.miss = True
        print(f'Changed Miss: {target.miss}')
    def remove(target):
        target.miss = False
    sun = Debuff('sun',apply,remove,2)
    prob = rd.random()
    print(prob)
    if prob <= 0.7:
        target.buffs.append(sun)
        


def blinding_lights(target,damage = 0):
    def apply(target):

        target.miss = True
        print(f'Changed Miss: {target.miss}')
    def remove(target):
        target.miss = False
    sun = Debuff('sun',apply,remove,2)
    prob = rd.random()
    print(prob)
    if prob <= 0.5:
        target.buffs.append(sun)

def bright_lights(target,damage = 0):
    def apply(target):

        target.miss = True
        print(f'Changed Miss: {target.miss}')
    def remove(target):
        target.miss = False
    sun = Debuff('sun',apply,remove,2)
    prob = rd.random()
    print(prob)
    if prob <= 0.3:
        target.buffs.append(sun)

def nice_guy(target,damage):
    target.damageEnemy(damage//2,'true')

def disco_inferno(target,damage):
    target.damageEnemy(damage//3, 'Fire')

def ricericebaby(target,damage):
    target.damageEnemy(damage//3,'Rice')

def waterloo(target,damage):
    target.damageEnemy(damage//3,'Water')

gameEffects =  {
    'theSun': (here_comes_the_sun,'Here Comes the Sun',50,'70% Chance to make the \nenemy miss the next attack'),
    'bLights': (blinding_lights,'Blinding Lights',30,'50% Chance to make the \nenemy miss the next attack'),
    'brightLights': (bright_lights,'Bright Lights',10,'30% Chance to make the \nenemy miss the next attack'),
    'niceguy': (nice_guy,'No More Mr.Nice Guy',100,"Deals additional true damage \nequal to half your \nweapon's damage"),
    'discoinferno': (disco_inferno,'Disco Inferno',50,"Deals additional fire damage\n equal to one third \nyour weapon's damage"),
    'ricericebaby': (ricericebaby,'Rice Rice Baby',50,"Deals additional rice damage\n equal to one third \nyour weapon's damage"),
    'waterloo': (waterloo,'Waterloo',50,"Deals additional water damage\n equal to one third \nyour weapon's damage")
}

def beyond(target):
    target.beyond = True

def bungieGum(target):
    target.bungieGum = True

playerEffects = {
    'beyond' : (beyond, 'Beyond...', 100,"Your attacks and effects \nare applied twice"),
    'bungieGum': (bungieGum,'Bungie Gum',70,"You can eat this weapon to \nheal or block the next attack")
}