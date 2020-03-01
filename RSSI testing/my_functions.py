from rflib import *
import time
import statistics as stat
import numpy as np
import datetime
import base64


# ==== DATA STRUCTURE ====

my_dtype = np.dtype({'names': ('roll', 'pitch', 'yaw', 'long', 'lat'),
                    'formats': ('f8', 'f8', 'f8', 'f8', 'f8')})

control_dtype = np.dtype({'names': ('left', 'right', 'up', 'down'),
                    'formats': ('b', 'b', 'b', 'b')})


# ==== Defining functions  ====


# Turns on receiver for dongle d and returns the received data


def RX_return(d):
    while True:
        try:
            y, z = d.RFrecv()
            if 'halt' in y:
                break
            else:
                return y
        except ChipconUsbTimeoutException:
            pass


# Turns on receiver for dongle d for t seconds and returns the received data


def RX_timer_return(t, d):
     timeout = time.time() + t
     while True:
        if time.time() > timeout:
            break
        try:
            y, z = d.RFrecv()
            if 'halt' in y:
                break
            else:
                return y
        except ChipconUsbTimeoutException:
            pass


# RSSI absolute power level (calculated using equation from C1110 manual)

def rssi_abs(d):
    rssi = ord(d.getRSSI())
    if rssi >= 128:
        rssi_dbm = ((rssi-256)/2) - 75 # 75 because of offset (adjust accordingly)
    else:
        rssi_dbm = (rssi/2) - 75
    return rssi_dbm

# Gets RSSI while listening out


def rssi_getter(d,received,rssi_av):
    rssi = []
    while True:
        try:
            rssi.append(rssi_abs(d))  # storing received rssi value
            y, z = d.RFrecv()
            if 'halt' in y:
                rssi_av.append(stat.mean(rssi))  # averaging rssi values
                break
            else:
                print y
                received.append(y)
        except ChipconUsbTimeoutException:
            pass


# ==== PROTOCOL ====

# Returns the data to be transmitted with the relevant addresses : destination add., device add, number of packets in sequence,  packet number (input in bytes)


def protocol_encaps_bytes(TXdata_bytes, dst_add, src_add, n_o_packets, packet_no):
    packet = struct.pack("3s3sii{}s".format(len(TXdata_bytes)), dst_add, src_add, n_o_packets, packet_no, TXdata_bytes)
    return packet

# Returns the data to be transmitted, split up (with relevant numbers),  with the relevant addresses and initial CRC value : destination add., device add., data length, data, CRC value and 'EOT'


def protocol_split_encaps(TXdata, dst_add, src_add, max_len):
    packets = []
    TXdata_bytes = TXdata.tobytes()
    TXdata_bytes_len = len(TXdata_bytes)
    if TXdata_bytes_len <= max_len:   # for short enough packets
        packets.append(protocol_encaps_bytes(TXdata_bytes, dst_add, src_add, 1, 1))
        return packets
    else:
        full_packet = TXdata_bytes_len // max_len
        residual_packet = TXdata_bytes_len % max_len
        if residual_packet == 0:
            for i in range(full_packet):
                TXdata_bytes_slice = TXdata_bytes[(i * max_len): ((i+1) * max_len)]
                packets.append(protocol_encaps_bytes(TXdata_bytes_slice, dst_add, src_add, full_packet, i+1))
            return packets
        else:
            for i in range(full_packet):
                TXdata_bytes_slice = TXdata_bytes[(i * max_len): ((i+1) * max_len)]
                packets.append(protocol_encaps_bytes(TXdata_bytes_slice, dst_add, src_add, full_packet + 1, i+1))
            TXdata_bytes_slice = TXdata_bytes[(full_packet * max_len):(full_packet * max_len) + residual_packet]
            packets.append(protocol_encaps_bytes(TXdata_bytes_slice, dst_add, src_add, full_packet + 1, full_packet +1))
            return packets

# as above but data already in bytes


def protocol_split_encaps_bytes(TXdata_bytes, dst_add, src_add, max_len):
    packets = []
    TXdata_bytes_len = len(TXdata_bytes)
    if TXdata_bytes_len <= max_len:   # for short enough packets
        packets.append(protocol_encaps_bytes(TXdata_bytes, dst_add, src_add, 1, 1))
        return packets
    else:
        full_packet = TXdata_bytes_len // max_len
        residual_packet = TXdata_bytes_len % max_len
        if residual_packet == 0:
            for i in range(full_packet):
                TXdata_bytes_slice = TXdata_bytes[(i * max_len): ((i+1) * max_len)]
                packets.append(protocol_encaps_bytes(TXdata_bytes_slice, dst_add, src_add, full_packet, i+1))
            return packets
        else:
            for i in range(full_packet):
                TXdata_bytes_slice = TXdata_bytes[(i * max_len): ((i+1) * max_len)]
                packets.append(protocol_encaps_bytes(TXdata_bytes_slice, dst_add, src_add, full_packet + 1, i+1))
            TXdata_bytes_slice = TXdata_bytes[(full_packet * max_len):(full_packet * max_len) + residual_packet]
            packets.append(protocol_encaps_bytes(TXdata_bytes_slice, dst_add, src_add, full_packet + 1, full_packet + 1))
            return packets

# Transmitting long split up data


def TX_long_data(TXdata, dst_add, dev_add, max_length, d):
    packets = protocol_split_encaps(TXdata, dst_add, dev_add, max_length)
    for packet in packets:
        # print 'before: ', datetime.datetime.now().time()
        d.RFxmit(packet)
        # print len(packet)
        # print 'after: ', datetime.datetime.now().time()
        # time.sleep(0.001)
        d.setModeIDLE()

# as above but data in bytes


def TX_long_data_bytes(TXdata, dst_add, dev_add, max_length, d):
    packets = protocol_split_encaps_bytes(TXdata, dst_add, dev_add, max_length)
    counter = 1
    for packet in packets:
        d.RFxmit(packet)
        print 'sent {} '.format(counter)
        counter += 1
        d.setModeIDLE()

# Extracts the data from the received data encapsulated in the protocol; has number of packets and packet number in the bunch


def protocol_extract_split(packet):
    data_len = len(packet) - 16
    try:
        data = struct.unpack("3s3sii{}s".format(data_len), packet)
        # if data[0] == dev_add:  # check if device is the intended receiver
        return data[4]
    except struct.error:
        print 'struct error'


#  Listens out for data and pieces together split up data, accounts for lost packets and returns the received string

def long_split_data(dev_add, packet, input_no_of_packets, d):
    received = ''
    received += protocol_extract_split(packet)  # data is extracted from packet and appended to 'received'
    # print protocol_extract_split(packet)
    for i in range(input_no_of_packets-1):  # for the remaining number of packets
        RXdata2 = RX_return(d)  # listen out for the next transmission
        if 'stop' in RXdata2:  # if stop in transmission it returns 'stop'
            return 'stop'
        preamble = struct.unpack('3s3sii', RXdata2[0:16])  # extracting the preamble data
        packet_no = preamble[3]
        intended_receiver = preamble[0]
        if intended_receiver == dev_add:  # check if device is the intended receiver
            if packet_no != i+2:  # if the packet is not sequentially correct
                received = None  # set received to None
                no_of_packets = preamble[2]
                print 'Missed packet'
                if packet_no == 1:  # If the packet is however the first of another transmission, restart this process
                    return long_split_data(dev_add, RXdata2, no_of_packets, d)
                else:
                    pass
            else:  # if packet is sequentially correct
                received += protocol_extract_split(RXdata2)  # data is extracted from packet and appended to 'received'
    return received


def receiving_long_split_data(dev_add, d):
    while True:
        RXdata = RX_return(d)
        if 'stop' in RXdata:
            break
        else:  # no stop
            preamble = struct.unpack('3s3sii', RXdata[0:16])  # extracting the preamble data
            no_of_packets = preamble[2]
            packet_no = preamble[3]
            intended_receiver = preamble[0]
            if intended_receiver == dev_add:  # check if device is the intended receiver
                if packet_no != 1:  # if not the first packet
                    received = None
                    print 'Missed packet'
                    return received
                elif packet_no == 1:  # if it is the first packet
                    received = long_split_data(dev_add, RXdata, no_of_packets, d)
                    if received == 'stop':  # accounts for missed packets followed by a 'stop'
                        break
                    else:
                        return received

# as above but with time limit

def receiving_long_split_data_timed(dev_add, wait_time , d):
    while True:
        RXdata = RX_timer_return(wait_time, d)
        if RXdata != None:
            if 'stop' in RXdata:
                break
            else:  # no stop
                preamble = struct.unpack('3s3sii', RXdata[0:16])  # extracting the preamble data
                no_of_packets = preamble[2]
                packet_no = preamble[3]
                intended_receiver = preamble[0]
                if intended_receiver == dev_add:  # check if device is the intended receiver
                    if packet_no != 1:  # if not the first packet
                        received = None
                        print 'Missed packet'
                        return received
                    elif packet_no == 1:  # if it is the first packet
                        received = long_split_data(dev_add, RXdata, no_of_packets, d)
                        if received == 'stop':  # accounts for missed packets followed by a 'stop'
                            break
                        else:
                            return received
        else:
            break


# returns True if interruption is successful and False for no/unsuccessful interruption


def interruption(wait_time, d):  # returns True if interruption is successful and False for no/unsuccessful interruption

    start = time.time()
    interrupt = RX_timer_return(wait_time, d)  # listens out for interruptions for t seconds
    end = time.time()

    t = end - start

    # print interruption

    if interrupt is None:  # for no interruptions
        print 'no interruption'
        return False
    elif 'INT' in interrupt:  # for an interruption
        print 'interrupted'
        time.sleep(.1)
        d.RFxmit('ACK'.ljust(50,'1'))  # send acknowledgement
        d.setModeRX()  # switch to RX
        confirmation = RX_timer_return(6, d) # listen out for confirmation for 6 seconds
        if confirmation is None:
            d.RFxmit('ERR'.ljust(50,'1'))
            print 'no acknowledgement'
            return False
        elif 'ACK' in confirmation:
            print 'acknowledgement received'
            return True
        elif 'ERR' in confirmation:
            print 'failed to receive'  # goes on to send the next bit of data
            return False
    else:
        print 'received something else'
        print interrupt
        if 0.5 < t < wait_time:
            return interruption(wait_time - t)
        else:
            return False

