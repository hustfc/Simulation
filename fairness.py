# -*- coding:utf-8 -*-

"传入所有中继设备的信息和选择的中继设备编号"


def Fairness(UES): 
    #计算当前状态的设备的公平状态

    U_total = 0
    U_link_s = 0     
    for i in range(0,len(UES)):
        U_total += UES[i].gains
        U_link_s += (1-UES[i].link_e)
    #加上采用第i个中继设备时的收益来计算fairness
    X=[]
    for i in range(0,len(UES)):
        Ui_overline = ((1-UES[i].link_e)/U_link_s)*U_total
        if UES[i].gains<=Ui_overline:
            X.append(UES[i].gains/Ui_overline)
        else:
            X.append(1.0)
    sum_of_xi = 0
    for i in range(0,len(X)):
        sum_of_xi += X[i]

    sum_of_xi2 = 0
    for i in range(0,len(X)):
        sum_of_xi2 += X[i]**2

    fairness = (sum_of_xi)**2/(len(X)*sum_of_xi2)
    # UES[x].fairness = fairness
    return fairness