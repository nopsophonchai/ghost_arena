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

gameEffects =  {
    'theSun': here_comes_the_sun,
    'bLights': blinding_lights,
    'brightLights': bright_lights,
    'niceguy': nice_guy,
    'discoinferno': disco_inferno
}