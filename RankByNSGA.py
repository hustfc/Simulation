# -*- coding:utf-8 -*-
import math
import random
import matplotlib.pyplot as plt
import json
import os



from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from EH.energy import energy
from Params.params import getDistance
from NewGame import game
import numpy as np
np.set_printoptions(suppress=True)
import thread
import threading
import time

# from fairness import Fairness #计算公平性指数的函数，第一个目标函数

global min_x
global max_x
class UE:
    count = 0
    def __init__(self, host, name, ip, port, link_e, gains=0.0, F_BS=0.0, F_UE=0.0, N1=0.0, b=0.0, Power = 0, rank=0, flag=False):
        self.host = host
        self.name = name
        self.ip = ip
        self.port = port
        self.link_e = link_e
        self.Power = random.uniform(0.003, 0.005)
        self.gains = 0
        UE.count += 1



'''
UES:是所有设备池
queue:候选满足传输能量的设备池
'''
def Fairness(UES,queue,x): #x表示的是传入设备的编号，也即染色体
    #传入的x是浮点数，要转化成整数
    x = int(round(x))
    U_total = 0
    U_link_s = 0     
    for i in range(0,len(UES)):
        U_total += UES[i].gains
        U_link_s += (1-UES[i].link_e)
    #加上采用第i个中继设备时的收益来计算fairness
    U_total += queue[x].F_UE
    X=[]
    for i in range(0,len(UES)):
        Ui_overline = ((1-UES[i].link_e)/U_link_s)*U_total
        if UES[i].name == queue[x].name:
            if (UES[i].gains+queue[x].F_UE)<=Ui_overline:
                X.append(UES[i].gains/Ui_overline)
            else:
                X.append(1.0)
        elif UES[i].gains<=Ui_overline:
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
#第二个目标函数，传输参数为序号
def Utility(queue,x):
    x= int(round(x))
    value = queue[x].F_BS
    return value

def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1
#按照function的值来排序
#list1的含义
def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1: #values中最小值的下标
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = float('inf')
    return sorted_list
#NSGA-II's fast non dominated sort,基于帕雷托最优解来计算支配解集
'''
输入：目标1数组，目标2数组

输出：前沿面数组，每一个前沿面中包含的是设备序号

'''
def fast_non_dominated_sort(values1, values2):
    S=[[] for i in range(0,len(values1))]
    front = [[]]
    n=[0 for i in range(0,len(values1))]
    rank = [0 for i in range(0, len(values1))]
    #对于目标1中的每一个解，计算其支配解集和支配解的个数
    for p in range(0,len(values1)):
        S[p]=[] #p的支配集合
        n[p]=0  #p的支配个数
        for q in range(0, len(values1)):
            #第p个设备的第一个目标大于q
            if  (values1[p] >= values1[q] and values2[p] > values2[q]) or (values1[p] > values1[q] and values2[p] >= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            #如果一个解被其他解所支配，那么其被支配数+1
            elif (values1[q] >= values1[p] and values2[q] > values2[p]) or (values1[q] > values1[p] and values2[q] >= values2[p]):
                n[p] = n[p] + 1
        #如果一个解的被支配数为0
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)
    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if( n[q]==0 ):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)
    del front[len(front)-1]
    return front
#采用解的距离有问题，不采用归一化两个目标之间距离差值太大，采用标准化，不能从初始值0开始
def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    #距离计算公式，换种定义
    for k in range(1,len(front)-1):
        if max(values1) == min(values1):
            maxdis = 1
        else:
            maxdis = max(values1)-min(values1)
        distance[k] = distance[k]+ (values1[sorted1[k+1]] - values1[sorted1[k-1]])/maxdis #统一标准化
    for k in range(1,len(front)-1):
        if max(values2) == min(values2):
            maxdis = 1
        else:
            maxdis = max(values2)-min(values2)
        distance[k] = distance[k]+ (values2[sorted2[k+1]] - values2[sorted2[k-1]])/maxdis
    return distance

#交叉
def crossover(a,b):
    r=random.random()
    if r>0.5:
        return mutation((a+b)/2)
    else:
        return mutation((a-b)/2)

#突变
def mutation(solution):
    global max_x
    mutation_prob = random.random()
    if max_x == min_x:
        maxdis = 1
    else:
        maxdis = max_x-min_x
    if mutation_prob <1:
        solution = min_x+maxdis*random.random()
    return solution

'''
排序函数,供考虑fairness时调用
输入：已知博弈信息后的设备池UES(已经按照基站的收益进行了排序)
计算：采用各个解能够达到的两个目标的大小来对各个中继设备来进行排序
输出:已经更新了Rank值的设备池UES

'''
def Rank(UES,queue):

    #只用求出所有中继设备的rank值不需要进行遗传求出最优解
    # obj1 = [Utility(i) for i in range(0,len(UES))]
    # obj2 = [Fairness(i) for i in range(0,len(UES))]
    # front = fast_non_dominated_sort(obj1[:],obj2[:])
    # print(front)
    # for i in range(0,len(front)):
    #     for j in range(0,len(front[i])):
    #         UES[front[i][j]].rank = i
    # # for i in range(0,len(UES)):
    # #     print(UES[i].rank)        
    # return UES
    '''
    在求解帕累托前沿面之前,将能量不充足的设备从解集中删除掉
    计算fairness的时候需要考虑的是所有设备的效益
    但是求解时不考虑
    '''
    pop_size = 20
    max_gen = 100
    #初始化
    global min_x
    global max_x
    min_x = 0
    max_x = len(queue)-1
    #random.random()产生一个(0,1)的随机数,此处在X范围内随机产生一个数
    solution=[min_x+(max_x-min_x)*random.random() for i in range(0,pop_size)] #产生从0到20设备编号解
    gen_no=0
    result=[]
    while(gen_no<max_gen):
        fairness_values = [Fairness(UES,queue,solution[i])for i in range(0,pop_size)]
        utility_values = [Utility(queue,solution[i])for i in range(0,pop_size)]
        
        # print(fairness_values)
    
        # print(utility_values)
        non_dominated_sorted_solution = fast_non_dominated_sort(utility_values[:],fairness_values[:])#快速非支配排序返回的front的集合
        # print("第",gen_no, "次繁衍的帕累托最优的设备编号为")
            
        # for valuez in non_dominated_sorted_solution[0]:
            # print(round(solution[valuez],3),end=" ")
        # print("\n")
        crowding_distance_values=[]
        for i in range(0,len(non_dominated_sorted_solution)):
            crowding_distance_values.append(crowding_distance(utility_values[:],fairness_values[:],non_dominated_sorted_solution[i][:]))
        solution2 = solution[:]
        #产生子代
        while(len(solution2)!=2*pop_size): #新一代种群数量是原种群数量的两倍
            a1 = random.randint(0,pop_size-1) #从种群中随机选择两个个体
            b1 = random.randint(0,pop_size-1)
            solution2.append(crossover(solution[a1],solution[b1]))#从原始的两个个体中交叉产生新的个体
        fairness_values2 = [Fairness(UES,queue,solution2[i])for i in range(0,2*pop_size)]
        utility_values2 = [Utility(queue,solution2[i])for i in range(0,2*pop_size)]
        non_dominated_sorted_solution2 = fast_non_dominated_sort(utility_values2[:],fairness_values2[:])
        crowding_distance_values2=[]
        for i in range(0,len(non_dominated_sorted_solution2)):
            crowding_distance_values2.append(crowding_distance(utility_values2[:],fairness_values2[:],non_dominated_sorted_solution2[i][:]))
        new_solution= []
        for i in range(0,len(non_dominated_sorted_solution2)):
            non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j],non_dominated_sorted_solution2[i]) for j in range(0,len(non_dominated_sorted_solution2[i]))]
            front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
            front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0,len(non_dominated_sorted_solution2[i]))]
            front.reverse()
            for value in front:
                new_solution.append(value)
                if(len(new_solution) == pop_size):
                    break
            if (len(new_solution) == pop_size):
                break
        solution = [solution2[i] for i in new_solution] # 最中求解出来的solution           
        result = solution 
        gen_no = gen_no + 1   
    IntResult = []
    for i in range(0,len(result)-1):
        IntResult.append(int(round(result[i],0)))
    #前沿面中随机选择一个点
    k = random.randint(0,len(IntResult)-1)
    
    return IntResult[k]


if __name__=='__main__':
    #创建网络和设备初始化
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference)
    #设备初始化
    ap1 = net.addAccessPoint('ap1', ssid="ap1-ssid", mode="g",
                             channel="1", position='5,6,0',range=40)
    AP = net.addStation('AP', position='5,10,0', ip='10.1.0.1', mac='00:00:00:00:00:EE') 

    UES = []
    for i in range(1,21):
        #创建中继设备节点
        temphost = net.addStation('DU%d'%i, position='%d,5,0'%(i+37), ip='10.0.0.%d'%i, mac='00:00:00:00:00:%02d'%i)
        #创建中继设备类对象
        temp = UE(temphost,'UE%d'%i,'10.0.0.%d'%i, 'DU%d-wlan0' %i,0.05+0.03*i) #丢包率已经初始化完毕
        UES.append(temp)

    for i in range(0,20):
            result = game(UES[i].link_e)
            UES[i].F_BS = result[2]
            UES[i].F_UE = result[3]
            UES[i].N1 = result[0]
            UES[i].b = result[1]
    #打印出设备池中的设备信息
    # for i in range(0,20):
    #     print(UES[i].name,UES[i].ip,UES[i].port,UES[i].Power,'\n')
    

    c0 = net.addController('c0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding Link\n")
    net.addLink(AP, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')
    for i in range(0,9):
        net.addLink(UES[i].host, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])

    #设备初始化完毕，开始进行调度
    #根据设备能够达到的基站的效益对所有中继设备进行排序
    queue = sorted(UES, key = lambda UE: UE.F_BS, reverse=True)

    #根据多目标优化方法对中继设备计算rank值（todo:只用rank作为排序有些不合理）
    '''
    在进行NSGA——II求解之前先判断能量是否足够传输,满足能量需求的中继设备才是候选解集
    '''
    len_que = len(queue)
    for i in range(0,len_que):
        if (queue[i].N1*0.00004) > queue[i].Power:
            del queue[i]
            len_que-=1

    num = Rank(UES,queue)
    print('select num',num)
