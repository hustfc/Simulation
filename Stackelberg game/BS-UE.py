import matplotlib.pyplot as plt
import numpy as np
from math import log

from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s)-1]
    s = s.replace(' ', '')
    # print(s)
    return [float(i) for i in s.split(',')]
File1 = 'Ulity.txt'
# x = [1,2,3,4,5,6,7,8,9,10,
#      11,12,13,14,15,16,17,18,19,20,
#      21,22,23,24,25,26,27,28,29,30,
#      31

#      ]
x = list(range(0, 32))
C = 3  # RU对包的基本支付单价
C_DU = 2  # DU传输一个包的成本
C_BS = 1  # BS传输一个包的成本
N = 32 #总包数
a = 2  # 满足因子
e = 0.1  # 丢包率
S = 1-e
# f1 = open(File1,'r')
# buffer1 = f1.readlines()
b = 8
y1 = []
y2 = []

for i in range(0,32):
    N1 = x[i]
    # temp1 = stringToList(buffer1[i][0:-1])
    U_DU = N1 * (C_BS + C * N * S / (log(a) * (a + S * N1))) - C_DU * N1
    # U_DU = N1 * b - C_DU * N1
    # U_BS = C * N * math.log(a + S * N1,a)-( C_BS + C * N * S / ( log(a) * (a + S * N1) ) )* N1 - (N - N1) * C_BS
    U_BS = C * N * math.log(a + S * N1, a) - b * N1 - (N - N1) * C_BS
    y1.append(U_DU)
    y2.append(U_BS)
plt.plot(x,y2,label="$U_{BS}$",marker='o',color="red",linewidth=2)#将$包围的内容渲染为数学公式
plt.plot(x,y1,"b--",marker='*',label="$U_{DU}$")
plt.xlabel("N1")
plt.ylabel("Utility")
plt.title("基站与中继设备效益随中继设备传输包数目N1变化曲线")
plt.ylim(0,300)
# plt.xlim(0,31)
plt.legend()#显示左下角的图例

plt.show()