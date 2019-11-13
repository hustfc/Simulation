# -*- coding:utf-8 -*-
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
        self.rank = 0
        UserEqu.Count += 1
#中继设备初始化
UE1 = UserEqu('UE1', '10.0.0.1', 0.10, 900, 195.43396778377053 , 78.65153714963657, 28, 5.808983469629878)
UE2 = UserEqu('UE2', '10.0.0.2', 0.15, 850, 225.13105279816864 , 100.58333991774799, 26, 6.868589996836461)
UE3 = UserEqu('UE3', '10.0.0.3', 0.20, 800, 247.54588421179346, 114.93967520628291, 24, 7.789153133595121)
UE4 = UserEqu('UE4', '10.0.0.4', 0.25, 750, 263.82627716639126, 125.27621813097173, 22, 8.694373551407805)
UE5 = UserEqu('UE5', '10.0.0.5', 0.30, 700, 281.2885847713523, 133.2092290621777, 21, 9.343296622008463)
UE6 = UserEqu('UE6', '10.0.0.6', 0.35, 650, 295.65261736458785, 139.53538286618212, 20, 9.976769143309106)
UE7 = UserEqu('UE7', '10.0.0.7', 0.40, 600, 307.3441330874717, 144.74137184593536, 19, 10.617966939259755)
UE8 = UserEqu('UE8', '10.0.0.8', 0.45, 550, 316.6832853264184, 149.12205673189075, 18, 11.284558707327264)
UE9 = UserEqu('UE9', '10.0.0.9', 0.50, 500, 323.907429967555, 152.86335767704668, 17, 11.991962216296864)

UES = [UE1,UE2,UE3,UE4,UE5,UE6,UE7,UE8,UE9]
#计算fairness的函数
def CalFairness(UES,UE):
    U_total = 0
    U_link_s = 0     
    for i in range(0,len(UES)):
        U_total += UES[i].gains
        U_link_s += (1-UES[i].link_e)
    #加上采用第i个中继设备时的收益来计算fairness
    U_total += UE.F_UE
    X=[]
    for i in range(0,len(UES)):
        Ui_overline = ((1-UES[i].link_e)/U_link_s)*U_total
        if UES[i].name == UE.name:
            if (UES[i].gains+UE.F_UE)<=Ui_overline:
                X.append(UES[i].gains/Ui_overline)
            else:
                X.append(1.0)
            # X.append((UES[i].gains + UE.F_UE)/Ui_overline)
        elif UES[i].gains<=Ui_overline:
            X.append(UES[i].gains/Ui_overline)
        else:
            X.append(1.0)
    print("X:",X)
    sum_of_xi = 0
    for i in range(0,len(X)):
        sum_of_xi += X[i]

    sum_of_xi2 = 0
    for i in range(0,len(X)):
        sum_of_xi2 += X[i]**2

    fairness = (sum_of_xi)**2/(len(X)*sum_of_xi2)
    UE.fairness = fairness
    return fairness

#计算两个解之间的距离
def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values1[sorted1[k+1]] - values2[sorted1[k-1]])/(max(values1)-min(values1))
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values1[sorted2[k+1]] - values2[sorted2[k-1]])/(max(values2)-min(values2))
    return distance


def dominate(U1,U2):
    if (U1.fairness>U2.fairness and U1.F_BS>=U2.F_BS) or (U1.fairness>=U2.fairness and U1.F_BS>U2.F_BS):
        return 1
    elif  (U1.fairness<U2.fairness and U1.F_BS<=U2.F_BS) or (U1.fairness<=U2.fairness and U1.F_BS<U2.F_BS):
        return -1
    else:
        return 0
#计算每个中继设备的rank值
def Rank(UES):
    for i in range(0,len(UES)):
        for j in range(0,len(UES)):
            if UES[i].name != UES[j].name:
                if dominate(UES[i],UES[j])<0:
                    UES[i].rank += 1
    return UES


if __name__ == '__main__':
#采用每一个中继设备就是一组解，分别计算采用各个中继设备时的fairness与U_BS
    for i in range(0,len(UES)):
        CalFairness(UES,UES[i])
    Rank(UES)
    for i in range(0,len(UES)):
        print(UES[i].name,' ',UES[i].rank,' ',UES[i].fairness,' ',UES[i].F_BS)

# U_BS = [i * -1 for i in function1_values]
# Fairness = [j * -1 for j in function2_values]
# plt.xlabel('U_BS', fontsize=15)
# plt.ylabel('Fairness', fontsize=15)
# plt.scatter(U_BS, Fairness)
# plt.show()