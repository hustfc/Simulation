from sympy import *
from math import pi

def LossRate_BS_FDS(Rk):
    y = Symbol('y')
    a = 3
    #Rk = 1
    f1 = y ** (2 / a - 1) * exp(-y)
    f2 = y ** (-2 / a) * exp(-y)
    I1 = integrate(f1, (y, 0, +oo))
    I2 = integrate(f2, (y, 0, +oo))
    Ca = (2 * pi / a) * I1 * I2
    ek = Ca * (Rk ** 2) * (3 ** (2 / a))
    nk = ((4 / 1000) / 1000) ** (2 / a)
    nk = nk * 5 / (10 ** 5)
    ek = ek * nk
    BSR = exp(-ek)
    #print("比特误码率", (1 - BSR))
    PLR = 1 - BSR ** 1024
    #print("丢包率", PLR * 100)
    print("距离: ", Rk, " ,比特误码率: ", (1 - BSR), " ,丢包率:", PLR * 100, "%")

def LossRate_FDS_RU(Rk):
    y = Symbol('y')
    a = 3
    #Rk = 1
    f1 = y ** (2 / a - 1) * exp(-y)
    f2 = y ** (-2 / a) * exp(-y)
    I1 = integrate(f1, (y, 0, +oo))
    I2 = integrate(f2, (y, 0, +oo))
    Ca = (2 * pi / a) * I1 * I2
    ek = Ca * (Rk ** 2) * (3 ** (2 / a))
    nk = 1 ** (2 / a)
    nk = nk * 5 / (10 ** 8)
    ek = ek * nk
    BSR = exp(-ek)
    #print("比特误码率", (1 - BSR))
    PLR = 1 - BSR ** 1024
    #print("丢包率", PLR * 100)
    print("距离: ", Rk, " ,比特误码率: ", (1 - BSR), " ,丢包率:", PLR * 100, "%")

RKS = list(range(41))

print("基站到雾设备的丢包率")
for i in RKS:
    LossRate_BS_FDS(i)
print("雾设备到RU的丢包率")
for i in RKS:
    LossRate_FDS_RU(i)



