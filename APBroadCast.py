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
    s = s.replace(' ', '')#是否要删除
    print(s)
    return [str(i) for i in s.split(',')]
''' 
为了适应时间线的功能现在每次发送一个编码之后的数据包
'''
def send(src, iface, dsts='', index = 0, pow = 5, send_pkt=[]):
    dsts = stringToList(dsts)
    num = len(dsts) #确定广播目标
    for i in range(0,num):
        print("dest%d:"% i,dsts[i])
    #由于send函数只能一对一发送，因此只能采取1对1模拟，每次广播一个数据包
    filename1 = '/home/shlled/mininet-project-duan/TimeSchedule/Log/msg.txt'#读取文件内容，只读取一次，以免开销过大
    f1=open(filename1,'r')
    buffer=f1.readlines()
    lenth=len(buffer)
    total=lenth
    for i in range(0,num): 
        #只发送一次
        time.sleep(1)
        dst = dsts[i]
        now = time.time()
        alpha=buffer[index] #读取文本对应位置内容
        msg = "send_time: " + "%.6f" % float(now)  + "total:%d" % total + "index:%d" % index + "data:" + alpha
        send_pkt.append(msg)
        print(msg) #此处打印出发送的内容
        p = Ether() / IP(src=src, dst=dst) / ICMP() / msg

        sendp(p, iface = iface)#组装好数据包之后发送数据

    f1.close()
    #重传部分，先不考虑，后面再考虑重传数据包"    
    
    #AP只考虑广播，并不考虑能量和收益"
fire.Fire(send)
