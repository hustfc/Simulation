import math
import json

class UserEqu:
    Count = 0
    def __init__(self, name, ip, link_e, gains, F_BS, F_UE, N1, b):
        self.name = name
        self.ip = ip 
        self.link_e = link_e
        self.gains = gains
        self.F_BS = F_BS
        self.F_UE = F_UE
        self.N1 = N1
        self.b = b
        UserEqu.Count += 1
UE1 =  UserEqu('UE1', '10.0.0.1', 0.1, 100, 195.43396778377053 , 78.65153714963657, 28, 5.808983469629878)
UE2 =  UserEqu('UE2', '10.0.0.2', 0.15, 100, 225.13105279816864 , 100.58333991774799, 26, 6.868589996836461)
UE3 =  UserEqu('UE3','10.0.0.3', 0.20, 100, 247.54588421179346, 114.93967520628291, 24, 7.789153133595121)

UES = [UE1,UE2,UE3]

#First function to optimize
if __name__=='__main__':
    for i in range(0,len(UES)):
        print(UES[i].name)