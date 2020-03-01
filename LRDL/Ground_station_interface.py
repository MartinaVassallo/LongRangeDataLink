from drone_gs_functions import *


dst_add = 'UAV'
dev_add = 'GST'
max_packet_len = 200
received = []

TXdata = np.array([(0, 0, 0, 1, 0), (1, 0, 0, 0, 0)], dtype=control_dtype)  # would contain a list of commands
# TXdata = []


ground_station(TXdata, dst_add, dev_add, max_packet_len, d)
