from my_functions import *
from YS1_configuration import *
import numpy as np
#
#
# TXdata = np.array([(2.43, 33.42, 8.23, 34.5645, 23.5345), (89.43, 3.42, 3.23, 34.5645, 23.5345), (9.43, 2.42, 8.23, 34.5645, 23.5345)], dtype=my_dtype)
#
#
# dst_add = 'MOO'
# src_add = 'BAA'
#
#
# TXdata_bytes = TXdata.tobytes()
# packet = struct.pack("3s3sii{}s".format(len(TXdata_bytes)), dst_add, src_add, 0, 1, TXdata_bytes)
#
# print len(packet)
# print struct.unpack("3s3sii", packet[0:16])
# a = struct.unpack("{}s".format(len(packet)-16), packet[16:len(packet)])
#
# print np.frombuffer(a[0], dtype=my_dtype)
#
# # print a
#

while True:
     d.RFxmit('1'.ljust(254,'1'))



# d.printRadioConfig(radiocfg=d.radiocfg)

# n=100
# a = True
#
# dst_add = 'GST'
# dev_add = 'UAV'
#????
# while a:
#
#     for i in range(len(TXdata)):
#         TX_long_data(TXdata[i], dst_add, dev_add, 200, d)  # transmits the data
#         # time.sleep(0.01)
#     # time.sleep(0.01)
#     d.RFxmit('stop')
#
#     d.setModeIDLE()  # sets mode to IDLE
#
#     print 'continue?'
#
#     a = int(raw_input())
raw_input
