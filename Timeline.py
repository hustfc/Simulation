# -*- coding:utf-8 -*-
'''
先采用1秒模拟1ms，所有文件sleep 1s 避免线程之间错乱
'''

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from EH.energy import energy
from Params.params import getDistance

import threading
import json
import random
from NewGame import game

"线程函数"
def command(host, arg):
    result = host.cmd(arg)
    return result


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid="ap1-ssid", mode="g",
                             channel="1", position='5,6,0',range=40)

    AP = net.addStation('AP', position='5,10,0', ip='10.0.0.1', mac='00:00:00:00:00:01')

    DU = net.addStation('DU', position='30,5,0', ip='10.0.0.2', mac='00:00:00:00:00:02')

    DU2 = net.addStation('DU2', position='15,15,0', ip='10.0.0.3', mac='00:00:00:00:00:03')

    DU3 = net.addStation('DU3', position='15,15,0', ip='10.0.0.4', mac='00:00:00:00:00:04')
    c0 = net.addController('c0')

    net.setPropagationModel(model="logDistance", exp=5)
    
    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding Link\n")
    net.addLink(AP, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(DU, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(DU2, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(DU3, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')
    
    info("*** Starting network ***\n")
    net.build()
    c0.start()
    ap1.start([c0]) 

    "划分时间线来确定每一时隙需要完成的任务"
    timeline = 0
    round = 0
    while(round<20):
        info("***first round AP collect the info\n***")
        try:
            thread.start_new_thread(command,(AP,"python RInfo.py 10.0.0.1 AP-wlan0"))
            thread.start_new_thread(command,(DU,"python SInfo.py 10.0.0.2 DU-wlan0 10.0.0.1"))
            thread.start_new_thread(command,(DU2,"python SInfo.py 10.0.0.3 DU2-wlan0 10.0.0.1"))
            thread.start_new_thread(command,(DU3,"python SInfo.py 10.0.0.4 DU3-wlan0 10.0.0.1"))
        except:
            print("info collect error")
        time.sleep(22)

    info("***AP start broadcasting ***\n")
    "DU,RU 随机接收信息还是接收能量"
    '''
    约束条件
    1.DU接收到的有效信息量比RU多博弈决策的N1
    2.DU的能量要能够保障在后一阶段能够发送足够的数据包
    
    计算出时隙比值来设置概率
    e1=0.4 e2=0.1
    '''
    p1 = 0.2 #DU1接收到但是RU没有接收到的概率，先设置为定值后再考虑与丢包率的关系，设置合理的丢包率
    p2 = 0.3 #DU2
    TotalTime = 10#时间片大小
    FileIndex = 0 #发送文件位置
    dst = ['10.0.0.2','10.0.0.3','10.0.0.4']
    for i in range(0,TotalTime):  #有100个最小时隙，AP广播100轮，DU选择接收能量和信息，RU直接接收信息  
        "此处AP应该改成广播，APsend 的 dst应该不止一个"  
        t1 = threading.Thread(target=command, args = (AP,"python APBroadCast.py 10.0.0.1 AP-wlan0 '%s' %s" %(dst,FileIndex)))#AP广播一个数据包
        t2 = threading.Thread(target=command, args = (RU,"python Receive.py 10.0.0.2 RU-wlan0 0.5"))
        top1 = int(100-100*p1)
        key1 = random.randint(1,100)
        "中继设备随机接收信息或者能量"
        #
        if key1 in range(1,top1):
            info("DU1 infomation\n")
            t3 = threading.Thread(target = command,args = (DU1,"python Receive.py 10.0.0.3 DU1-wlan0 0.1"))
        else:
            info("DU1 energy\n")
            t3 = threading.Thread(target = energy,args = (DU1,AP,1))
        t3.start()

        top2 = int(100-100*p2)
        key2 = random.randint(1,100)

        if key2 in range(1,top2):
            info("DU2 infomation\n")
            t4 = threading.Thread(target=command,args=(DU2,"python Receive.py 10.0.0.4 DU2-wlan0 0.2"))
        else:
            info("DU2 energy\n")
            t4 = threading.Thread(target = energy,args = (DU2,AP,1) )
        t4.start()
        #先开始监听进程再开始发送进程
        t2.start()
        t1.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        FileIndex += 1 
    
    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
