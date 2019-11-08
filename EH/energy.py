# -*- coding:utf-8 -*-
from numpy import random
import math
from mininet.log import info
import json
# from mn_wifi import propagationModels
# from random import gauss


#根据relay的发射功率来计算中继的损耗
#中继的发射功率一般比较小
#基站 45w 中继3.2mW
def energy(sta, ap, time):
    #没有想好energy harvest
    staPosition = sta.params['position'][0:2]
    # num = str(sta)[2]
    apPosition = ap.params['position'][0:2]
    distance = math.sqrt((staPosition[0] - apPosition[0]) ** 2 + (staPosition[1] - apPosition[1]) ** 2)
    # info('distance : %.2f m\n' % distance)
    # txpower = float(ap.params['txpower'][0]) #根据基站的发射功率计算能量收集
    # info('txpower: %.3f dbm\n' % txpower)  #dbm转化成w
    
    #transmitPower = 10 ** (txpower / 10) / 1000
    transmitPower = 20 #基站的发射功率

    # info('transmitPower: %f W\n' % transmitPower) 
    
    alpha = 2.0
    t, receiveEnergy = 0, 0
    interval = 0.0001
    while t <= time:
        h = random.normal(0, 1)
        receivePower = transmitPower * (distance ** (-alpha)) * (h ** 2)
        print('receive power',receivePower)
        receiveEnergy += receivePower * interval
        t += interval
    # info('after %fs receive energy : %fJ\n' % (time, receiveEnergy))
    pow = float(receiveEnergy)
    return pow
    # filename = "/home/shlled/mininet-project-duan/TimeSchedule/Log/DU%c.json" % num
    # with open(filename,'r+') as f:
    #     buffer = f.readlines()
    #     lenth = len(buffer)            
    #     data = json.loads(buffer[-1])
    #     data["POWER"] += pow
    #     json.dump(data,f)
    #     f.write("\n")