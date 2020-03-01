from my_functions import *
from YS1_configuration import *
import matplotlib.pyplot as plt
from statistics import mean
import csv


distance_vs_dBm = []

while True:
    dbm = []

    print 'input distance'

    distance = raw_input()

    if distance == 'stop':
        break

    i=0

    d.setModeRX()
    d.setMdmDeviatn(RX_dev)

    timeout = time.time() + 30
    
    while True:

        if time.time() > timeout:
            break

        y = rssi_abs(d) # getting the power value
        if y<-100:
            continue
        else:
            dbm.append(y)

    distance_vs_dBm.append([int(distance), mean(dbm)])


with open('distance_vs_power(dBm)_telescopic_ant3.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(distance_vs_dBm)
csvFile.close()
