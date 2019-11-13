import matplotlib.pyplot as plt
from pylab import *
# mpl.rcParams['font.sans-serif'] = ['SimHei']
from sympy import  *
from math import log
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 16}) # 改变所有字体大小，改变其他性质类似
def game(N,S,C_BS):
    C = 5 #RU对包的基本支付单价
    C_DU = 2 #DU传输一个包的成本
    # C_BS = 1  #BS传输一个包的成本
    # N = 32 #总包数
    a = 2  #满足因子
    # e = 0.1  #丢包率
    x = Symbol('x')
    # expr1 = x*(C_BS+(C*N*S)/(log(a)*(a+S*x)))
    expr1 = C_BS + C*N*S/(log(a)*(a+S*x))+x*(-C*N*S*S)/(log(a)*(a+S*x)*(a+S*x))-C_DU
    # N1 = solve(diff(expr1,x),x)
    ans = solve(expr1,x)
    lenth = len(ans)
    N1 = ans[0]

    for i in range(0,lenth):
        if ans[i]>0:
            N1 = ans[i]
    if N1>0:
        temp = int(N1)
    else:
        N1 = 0
        temp = 0
    U_L = temp * (C_BS + C*N*S/(log(a)*(a+S*temp)))-C_DU*temp #向下取整的时候的效益
    temp = temp+1
    U_H = temp * (C_BS + C*N*S/(log(a)*(a+S*temp)))-C_DU*temp #向上取整的时候的效益
    if U_L>U_H:
        N1 = temp -1
        U_DU = U_L
    else:
        N1 = temp
        U_DU = U_H
    b = C_BS + C*N*S/(log(a)*(a+S*N1))
    U_BS = C*N*log(a+S*N1, a)-b*N1-(N-N1)*C_BS
    result = [N1,b,U_BS,U_DU]
    filename = 'cbs%f.txt'% C_BS
    with open(filename,'a+') as f:
        f.write(str(result))
        f.write('\n')
    return result
def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s)-1]
    s = s.replace(' ', '')
    # print(s)
    return [float(i) for i in s.split(',')]
File1 = 'cDU2.txt'
File2 = 'cDU3.txt'
File3 = 'cDU4.txt'
File4 = 'cDU5.txt'
# File5 = 'cbs1.500000.txt'

# x=np.linspace(0,32,1)#X轴数据
x = [1,2,3,4,5,6,7,8,9,10,
     11,12,13,14,15,16,17,18,19,20,
     21,22,23,24,25,26,27,28,29,30,
     31]
if __name__ == '__main__':
    # 产生数据
    # c = [1]
    # for i in range(0,1):
    #     for j in range(1,32):
    #         game(j,0.1,c[i])
    #绘制图
    f1 = open(File1, 'r')
    f2 = open(File2, 'r')
    f3 = open(File3, 'r')
    f4 = open(File4, 'r')
    # f5 = open(File5, 'r')
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []

    y6 = []
    y7 = []
    y8 = []
    y9 = []
    y10 = []

    buffer1 = f1.readlines()
    buffer2 = f2.readlines()
    buffer3 = f3.readlines()
    buffer4 = f4.readlines()
    # buffer5 = f5.readlines()

    for i in range(0, 31):
        temp1 = stringToList(buffer1[i][0:-1])
        temp2 = stringToList(buffer2[i][0:-1])
        temp3 = stringToList(buffer3[i][0:-1])
        temp4 = stringToList(buffer4[i][0:-1])
        # temp5 = stringToList(buffer5[i][0:-1])

        t1 = temp1[2]#c_du =1
        y1.append(t1)
        t6 = temp1[3]
        y6.append(t6)

        t2 = temp2[2]#c_du = 2
        y2.append(t2)
        t7 = temp2[3]
        y7.append(t7)

        t3 = temp3[2]
        y3.append(t3)
        t8 = temp3[3]
        y8.append(t8)

        t4 = temp4[2]
        y4.append(t4)
        t9 = temp4[3]
        y9.append(t9)
        #
        # t5 = temp5[2]
        # y5.append(t5)
        # t10 = temp5[3]
        # y10.append(t10)


    plt.figure(figsize=(8, 4))

    plt.plot(x, y1, label="$case3:U_{BS}$", marker='^', markersize='4', color="teal", linewidth=1)
    plt.plot(x, y2, label="$case4:U_{BS}$", marker='^', markersize='4', color="royalblue", linewidth=1)
    plt.plot(x, y3, label="$case5:U_{BS}$", marker='^', markersize='4', color='goldenrod', linewidth=1)
    plt.plot(x, y4, label= "$case6:U_{BS}$",marker = '^',markersize = '4',color = 'black',linewidth = 1)
    # plt.plot(x, y5, label= "$case5:U_{BS}$",marker = '^',markersize = '4',color = 'red',linewidth = 1)

    plt.plot(x, y6, marker='x', markersize='4', color="teal", label="$case3:U_{FD}$", linestyle=':')
    plt.plot(x, y7, marker='x', markersize='4', color="royalblue", label="$case4:U_{FD}$", linestyle=':')
    plt.plot(x, y8, marker='x',markersize = '4', color="goldenrod", label="$case5:U_{FD}$", linestyle=':')
    plt.plot(x, y9, marker= 'x',markersize = '4',color = 'black',label = "$case6:U_{FD}$",linestyle = ':')
    # plt.plot(x, y10, marker='x', markersize='4', color='red', label="$case5:U_{FD}$", linestyle= ':')
    # # 指定曲线的颜色和线性，如‘b--’表示蓝色虚线（b：蓝色，-：虚线）

    plt.xlabel("N")
    plt.ylabel("Utility")
    # plt.title("Variations of Utility of BS and RD with $C_{BS}$")
    f1.close()
    f2.close()
    f3.close()
    # f4.close()
    # f5.close()
    '''
    使用关键字参数可以指定所绘制的曲线的各种属性：
    label：给曲线指定一个标签名称，此标签将在图标中显示。如果标签字符串的前后都有字符'$'，则Matplotlib会使用其内嵌的LaTex引擎将其显示为数学公式
    color：指定曲线的颜色。颜色可以用如下方法表示
        英文单词
        以‘#’字符开头的3个16进制数，如‘#ff0000’表示红色。
        以0~1的RGB表示，如（1.0,0.0,0.0）也表示红色。
    linewidth：指定权限的宽度，可以不是整数，也可以使用缩写形式的参数名lw。
    '''
    plt.text(100,0,'Variations with $C_{BS}$',verticalalignment="bottom",horizontalalignment="center")
    # plt.ylim(0, 270)
    # plt.xlim(0,31)
    plt.legend(ncol=2)  # 显示左下角的图例
    plt.show()

# C = 3  # RU对包的基本支付单价
# C_DU = 2  # DU传输一个包的成本
# C_BS = 1  # BS传输一个包的成本
# N = 32 #总包数
# a = 2  # 满足因子
#
#
# #绘制折线图
# plt.plot(e, U_BS_ES, marker = '*', color = 'black', label = 'ES')
# plt.plot(e, U_BS_Non, marker= 'o', linestyle=':', color='black', label = 'Non-ES')
#
# plt.xlabel("loss rate")
# plt.xlim(0,1)
# plt.ylabel("Utility of BS")
# # plt.title("不采用中继（Non-ES）与采用中继博弈均衡（ES）时基站效益对比图")
# plt.legend()
# plt.show()