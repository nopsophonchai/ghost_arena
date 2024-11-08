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
    target.damageEnemy(damage//3, 'fire')

def ricericebaby(target,damage):
    target.damageEnemy(damage//3,'rice')

def waterloo(target,damage):
    target.damageEnemy(damage//3,'water')

gameEffects =  {
    'theSun': (here_comes_the_sun,'Here Comes the Sun',20),
    'bLights': (blinding_lights,'Blinding Lights',10),
    'brightLights': (bright_lights,'Bright Lights',10),
    'niceguy': (nice_guy,'No More Mr.Nice Guy',30),
    'discoinferno': (disco_inferno,'Disco Inferno',20)
}

def beyond(target):
    target.beyond = True

def bungieGum(target):
    target.bungieGum = True

playerEffects = {
    'beyond' : (beyond, 'Beyond...', 30),
    'bungieGum': (bungieGum,'Bungie Gum',20)
}