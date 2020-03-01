from my_functions import *
from YS1_configuration import *
import csv
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import math


distance_vs_dBm = []

dbm = []


d.setModeRX()

timeout = time.time() + 30
while True:

    if time.time() > timeout:
        break

    y = rssi_abs(d) # getting the power value
    if y<-100:
        continue
    else:
        dbm.append(y)

t = np.linspace(0, 30, len(dbm))

print mean(dbm)

dbm_std = np.std(dbm)
dbm_sem = dbm_std/math.sqrt(len(dbm))
dbm_err = 1.96*dbm_sem

print dbm_err

plt.plot(t, dbm)
plt.show()



# with open('RSSI_point_distribution.csv', 'w') as csvFile:
#         writer = csv.writer(csvFile)
#         writer.writerows(distance_vs_dBm)
# csvFile.close()
