from mininet.log import info
from sympy import *
from math import pi

def LossRate_FDS_RU(FD, RU):
    # 初始化坐标和距离
    FDPosition = FD.params['position'][0:2]
    RUPosition = RU.params['position'][0:2]
    distance = math.sqrt((FDPosition[0] - RUPosition[0]) ** 2 + (FDPosition[1] - RUPosition[1]) ** 2)

    # 计算丢包率
    y = Symbol('y')
    a = 3
    f1 = y ** (2 / a - 1) * exp(-y)
    f2 = y ** (-2 / a) * exp(-y)
    I1 = integrate(f1, (y, 0, +oo))
    I2 = integrate(f2, (y, 0, +oo))
    Ca = (2 * pi / a) * I1 * I2
    ek = Ca * (distance ** 2) * (3 ** (2 / a))
    nk = 1 ** (2 / a)
    nk = nk * 5 / (10 ** 8)
    ek = ek * nk
    BSR = exp(-ek)
    # print("比特误码率", (1 - BSR))
    PLR = 1 - BSR ** 1024
    # print("丢包率", PLR * 100)
    print("距离: ", distance, " ,比特误码率: ", (1 - BSR), " ,丢包率:", PLR * 100, "%")