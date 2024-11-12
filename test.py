import random as rd
list = [1,2,1,2,3]

list.pop(rd.randint(0,len(list)-1))
print(list)