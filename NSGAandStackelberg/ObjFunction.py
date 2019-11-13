import math

#目标函数
def GrieFunc(vardim, x, bound):
    """
    Griewangk function
    经典函数girewangk
    """
    s1 = 0.
    s2 = 1.
    for i in range(1, vardim + 1):
        s1 = s1 + x[i - 1] ** 2
        s2 = s2 * math.cos(x[i - 1] / math.sqrt(i))
    y = (1. / 4000.) * s1 - s2 + 1
    y = 1. / (1. + y)
    return y

#非凸优化函数
def RastFunc(vardim, x, bound):
    """
    Rastrigin function
    在数学优化中，Rastrigin函数是一个非凸函数，用作优化算法的性能测试问题。这是一个非线性多模态函数的典型例子。它最初由Rastrigin [1]提出作为二维函数，并已被Mühlenbein等人推广。[2]寻找这个函数的最小值是一个相当困难的问题，因为它有很大的搜索空间和大量的局部最小值。
在一个n维域上，它被定义为：
{\ displaystyle f（\ mathbf {x}）= An + \ sum _ {i = 1} ^ {n} \ left [x_ {i} ^ {2} -A \ cos（2 \ pi x_ {i}）\对]} f（\ mathbf {x}）= An + \ sum _ {i = 1} ^ {n} \ left [x_ {i} ^ {2} -A \ cos（2 \ pi x_ {i}）\ right]
    """
    s = 10 * 25
    for i in range(1, vardim + 1):
        s = s + x[i - 1] ** 2 - 10 * math.cos(2 * math.pi * x[i - 1])
    return s