# -*- coding:utf-8 -*-
from mininet.log import info
from sympy import *
from math import pi, sqrt

def LossRate_FDS_RU(FD, RU):
    # 初始化坐标和距离
    FDPosition = FD.params['position'][0:2]
    RUPosition = RU.params['position'][0:2]
    distance = sqrt((FDPosition[0] - RUPosition[0]) ** 2 + (FDPosition[1] - RUPosition[1]) ** 2)

    # 计算丢包率
    y = Symbol('y')
    a = 3.0
    f1 = y ** (2.0 / a - 1) * exp(-y)
    f2 = y ** (2.0 / a - 1) * exp(-y)
    I1 = integrate(f1, (y, 0, oo))
    I2 = integrate(f2, (y, 0, oo))
    Ca = (2.0 * pi / a) * I1 * I2
    ek = Ca * (distance ** 2.0) * (3.0 ** (2.0 / a))
    nk = 1.0 ** (2.0 / a)
    nk = nk * 5.0 / (10.0 ** 8)
    ek = ek * nk
    BSR = exp(-ek)
    # print("比特误码率", (1 - BSR))
    PLR = 1 - BSR ** 1024
    # print("丢包率", PLR * 100)
    info("distance : %f, bit error rate: %3f, packet loss rate: %3f \n" % (distance, 1 - BSR, PLR))
    # print("distance", distance, " ,bit error rate: ", (1 - BSR), " ,packet loss rate:", PLR * 100, "%")
    return PLR