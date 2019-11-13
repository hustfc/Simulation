# -*- coding:utf-8 -*-
import numpy as numpy
from sympy import  *
from math import log

'''
新的博弈模型
'''
def game(S,N):
    C = 5 #RU对包的基本支付单价
    C_DU = 3 #DU传输一个包的成本
    C_BS = 1  #BS传输一个包的成本
    #N = 1 #总包数
    a = 2  #满足因子
    e = 0.1  #丢包率
    x = Symbol('x')
    # expr1 = x*(C_BS+(C*N*S)/(log(a)*(a+S*x)))
    expr1 = C_BS + C*N*S/(log(a)*(a+S*x))+x*(-C*N*S*S)/(log(a)*(a+S*x)*(a+S*x))-C_DU
    # N1 = solve(diff(expr1,x),x)
    ans = solve(expr1,x)
    lenth = len(ans)
    N1 = ans[0]
    print('dad', ans)
    for i in range(0,lenth):
        if ans[i]>0:
            N1 = ans[i]
    if N1>0:
        temp = int(N1)
    else:
        N1 = 0
        temp = 0
    U_L =temp * (C_BS + C*N*S/(log(a)*(a+S*temp)))-C_DU*temp #向下取整的时候的效益
    temp = temp+1
    U_H = temp * (C_BS + C*N*S/(log(a)*(a+S*temp)))-C_DU*temp #向上取整的时候的效益
    if U_L>U_H:
        N1 = temp -1
        U_DU = U_L
    else:
        N1 = temp
        U_DU = U_H
    b = C_BS + C*N*S/(log(a)*(a+S*N1))
    # print('dadad',b)
    U_BS = C*N*log(a+S*N1, a)-b*N1-(N-N1)*C_BS
    result = [N1,b,U_BS,U_DU]
    filename = 'Solution.txt'
    with open(filename,'a+') as f:
        f.write(str(result))
        f.write('\n')
    print(result)
    # return result
if __name__ == '__main__':
    for i in range(0,11):
        game(0.52+i*0.02,32)
