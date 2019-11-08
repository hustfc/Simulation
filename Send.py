# -*- coding: utf8 -*-

from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField
from scapy.all import Ether, IP, ICMP
from mininet.log import info

import time

import sys
import fire
import json
import random
def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s)-1]
    s = s.replace(' ', '')
    print(s)
    return [int(i) for i in s.split(',')]
''' 
为了适应时间线的功能现在每次发送一个编码之后的数据包
'''
def send(src, iface, dst, distance, pow, gain, index,send_pkt=[]):
    pow = 0.004
    time.sleep(1)
    if distance <= 4:
        loss = 0
    elif distance <=10:
        loss = 0.1
    else:
        loss = 0.4
    index = int(index) #确定每次传输的index
    filename1 = '/home/shlled/mininet-project-duan/TimeSchedule/Log/msg.txt'
    f1=open(filename1,'r')
    buffer=f1.readlines()
    lenth=len(buffer)
    total=lenth

    "只发送一次"
    now = time.time()
    alpha=buffer[index] #读取文本对应位置内容
    msg = "send_time: " + "%.6f" % float(now)  + "total:%d" % total + "index:%d" % index + "data:" + alpha
    send_pkt.append(msg)
    print(msg)
    p = Ether() / IP(src=src, dst=dst) / ICMP() / msg
    "一定概率不发送数据包"
    top=int(100-100*loss)
    key=random.randint(1,100)
    if key in range(1,top):
        sendp(p, iface = iface)
    else:
        print("can't send the packet\n")
    f1.close()
    "重传部分，先不考虑，后面再考虑重传编码包"    
    
    "在传输结束之后，进行能量和收益的更新"
    filename2='/home/shlled/mininet-project-duan/TimeSchedule/Log/DU%s.json' % src[7:8]
    with open(filename2,'r+') as f2:
        buffer = f2.readlines()
        lenth = len(buffer)            
        data = json.loads(buffer[lenth-1])
        data["POWER"] -= pow
        data["Gains"] += gain 
        # integ =  count / total
        # data["Integrity"] = integ
        json.dump(data,f2)
        f2.write("\n")
fire.Fire(send)
