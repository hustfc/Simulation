# -*- coding: utf8 -*-
from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField
from mininet.log import info

import sys
import struct
import time
from collections import Counter
import fire
import random
import re
import os

packet_counts = Counter()
packet_queue = []
global Tloss #丢包率临时变量
class action:
    def __init__(self, IP, rc_pkt):
        self.ip = IP
        self.rc_pkt = rc_pkt

    def custom_action(self, packet):
        key = tuple([packet[0][1].src, packet[0][1].dst])
        if packet[0][1].dst == self.ip:  
            #将数据写入到缓存文件中
            filename = '/home/shlled/mininet-project-duan/TimeSchedule/Log/%s.txt' % packet[0][1].dst[7:8]
            f1 = open(filename, "a+")
            packet_queue.append(packet[0][3].load)
            self.rc_pkt.append(packet[0][3].load)
            packet_counts.update([key])
            now = time.time()
            #缓存中写入了才表示实际接收到了该数据包,根据丢包率来确定是否实际接收到了该数据包
            global Tloss
            loss = Tloss
            top = int(100-100*loss)
            key = random.randint(1,100)
            if key in range(1,top):
                info = "receive_time: " + "%.6f" % float(now) + " " + packet[0][3].load
                print("info in action :", info)
                f1.write('Receive Packet #%d: %s ==> %s : %s' % (
                    sum(packet_counts.values()), packet[0][1].src, packet[0][1].dst, info))
            f1.close()
        sys.stdout.flush()
#loss 表示丢包率
def receive(ip, iface, loss,filter="icmp", rc_pkt=[]):
    global Tloss
    Tloss = loss
    sniff(iface=iface, filter="icmp", timeout=10, prn=action(ip, rc_pkt).custom_action)
    #在sniff之后可以查看哪些编码包序号的被接收到了

def packetQueue():
    print(packet_counts)
    print(packet_queue)

fire.Fire(receive)
