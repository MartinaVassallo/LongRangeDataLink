import sys
from rflib import *
import time
from my_functions import *
import matplotlib.pyplot as plt
from YS1_configuration import *
from statistics import mean


d.setModeRX()

i=0
rs = []

while True:
    plt.ion()
    plt.show()
    plt.title('power vs progression')
    plt.ylabel('Absolute power (dBm)')

    y = rssi_abs(d) # getting the RSSI value
    rs.append(y)
    x = i
    i += 1
    
    plt.scatter(x, y, marker='.', s=15, color='blue')
    plt.pause(0.0001)

