import matplotlib.pyplot as plt
import numpy as np
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s)-1]
    s = s.replace(' ', '')
    # print(s)
    return [float(i) for i in s.split(',')]
File1 = 'Ulity11.txt'
File2 = 'Ulity12.txt'
File3 = 'Ulity13.txt'
File4 = 'Ulity14.txt'
File5 = 'Ulity15.txt'
# x=np.linspace(0,32,1)#X轴数据
x = [1,2,3,4,5,6,7,8,9,10,
     11,12,13,14,15,16,17,18,19,20,
     21,22,23,24,25,26,27,28,29,30,
     31
     ]
f1 = open(File1, 'r')
f2 = open(File2, 'r')
f3 = open(File3, 'r')
f4 = open(File4, 'r')
f5 = open(File5, 'r')

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
buffer5 = f5.readlines()
for i in range(0,31):
    temp1 = stringToList(buffer1[i][0:-1])
    temp2 = stringToList(buffer2[i][0:-1])
    temp3 = stringToList(buffer3[i][0:-1])
    temp4 = stringToList(buffer4[i][0:-1])
    temp5 = stringToList(buffer5[i][0:-1])
    t1 = temp1[2]
    y1.append(t1)
    t6 = temp1[3]
    y6.append(t6)

    t2 = temp2[2]
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

    t5 = temp5[2]
    y5.append(t5)
    t10 = temp5[3]
    y10.append(t10)
# print('1 ',len(y1))
# print('2 ',len(y2))
# print('3 ',len(y3))
# print('4 ',len(y4))
# print('5 ',len(y5))
# print('6 ',len(y6))
plt.figure(figsize=(8,4))

plt.plot(x,y1,label="$U_{BS}1$",marker='o',color="red",linewidth=1)#
plt.plot(x,y6,marker='*', color="red", label="$U_{DU}1$", linestyle=':')

plt.plot(x,y2,label="$U_{BS}2$",marker='o',color="blue",linewidth=1)#
plt.plot(x,y7,marker='*', color="blue", label="$U_{DU}2$", linestyle=':')

plt.plot(x,y3,label="$U_{BS}3$",marker='o',color="green",linewidth=1)#
plt.plot(x,y8,marker='*', color="green", label="$U_{DU}3$", linestyle=':')

plt.plot(x,y4,label="$U_{BS}4$",marker='o',color="aqua",linewidth=1)#
plt.plot(x,y9,marker='*', color="aqua", label="$U_{DU}4$", linestyle=':')

plt.plot(x,y5,label="$U_{BS}5$",marker='o', color="gray",linewidth=1)#
plt.plot(x,y10,marker='*', color="gray", label="$U_{DU}5$", linestyle=':')
#指定曲线的颜色和线性，如‘b--’表示蓝色虚线（b：蓝色，-：虚线）

plt.xlabel("N")
plt.ylabel("Utility")
plt.title("基站与中继设备效益图")
f1.close()
f2.close()
f3.close()
'''
使用关键字参数可以指定所绘制的曲线的各种属性：
label：给曲线指定一个标签名称，此标签将在图标中显示。如果标签字符串的前后都有字符'$'，则Matplotlib会使用其内嵌的LaTex引擎将其显示为数学公式
color：指定曲线的颜色。颜色可以用如下方法表示
       英文单词
       以‘#’字符开头的3个16进制数，如‘#ff0000’表示红色。
       以0~1的RGB表示，如（1.0,0.0,0.0）也表示红色。
linewidth：指定权限的宽度，可以不是整数，也可以使用缩写形式的参数名lw。
'''

plt.ylim(0,500)
# plt.xlim(0,31)
plt.legend()#显示左下角的图例

plt.show()