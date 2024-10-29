import random as rd

# def beyond(weapon):



def here_comes_the_sun(target,damage = 0):
    if rd.random() < 0.7:
        target.miss = True

def blinding_lights(target,damage = 0):
    if rd.random() < 0.5:
        target.miss = True

def bright_lights(target,damage = 0):
    if rd.random() < 0.3:
        target.miss = True

def nice_guy(target,damage):
    target.damageEnemy(damage//2,'True')

def disco_inferno(target,damage):
    target.damageEnemy(damage//3, 'Fire')

gameEffects =  {
    'theSun': here_comes_the_sun,
    'bLights': blinding_lights,
    'brightLights': bright_lights,
    'niceguy': nice_guy,
    'discoinferno': disco_inferno
}