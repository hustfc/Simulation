from sympy import *
from math import pi

def LossRate(Rk):
    y = Symbol('y')
    a = 4
    #Rk = 1
    f1 = y ** (2 / a - 1) * exp(-y)
    f2 = y ** (-2 / a) * exp(-y)
    I1 = integrate(f1, (y, 0, +oo))
    I2 = integrate(f2, (y, 0, +oo))
    Ca = (2 * pi / a) * I1 * I2
    ek = Ca * (Rk ** 2) * (3 ** (2 / a))
    nk = ((4 / 1000) / 20) ** (2 / a)
    nk = nk * 5 / (10 ** 6)
    ek = ek * nk
    BSR = exp(-ek)
    #print("比特误码率", (1 - BSR))
    PLR = 1 - BSR ** 1024
    #print("丢包率", PLR * 100)
    print("距离: ", Rk, " ,比特误码率: ", (1 - BSR), " ,丢包率:", PLR * 100, "%")

RKS = list(range(41))
for i in RKS:
    LossRate(i)



