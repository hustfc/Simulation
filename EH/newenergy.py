# -*- coding:utf-8 -*-
from numpy import random
import math
from mininet.log import info
import json

'''

'''

def energy(sta, ap, time):
    
    staPosition = sta.params['position'][0:2]

    apPosition = ap.params['position'][0:2]

    d = math.sqrt((staPosition[0] - apPosition[0]) ** 2 + (staPosition[1] - apPosition[1]) ** 2)
    # print('distance:',d)
    # todo:功率变化
    P_t = 6000
    G_T = 2
    G_R = 2
    c = 300000000.0 
    lamda = c/900000000.0
    L = 0.8
    P_R = P_t*G_T*G_R*(lamda**2)/(L*(4*math.pi*d)**2)

    # print('receive power',P_R)
    power = P_R * time
    # print('energy',power)
    return power 

# if __name__ == '__main__':
#     energy(6000,32,0.011)