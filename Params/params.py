import math
from mininet.log import info

def getDistance(h1, h2):
    distance = math.sqrt((int(h1.params['position'][0]) - int(h2.params['position'][0])) ** 2 + (int(h1.params['position'][1]) - int(h2.params['position'][1])) ** 2)
    return distance