from my_functions import *
from YS1_configuration import *


# ==== DRONE ====

def drone(TXdata, dst_add, dev_add, max_length, d, i=0):  # when the function is called, the value of i is set to 0
    ON = 1
    while True:
        try:
            print 'transmitting'

            d.setModeIDLE()

            time.sleep(0.1)

            if isinstance(TXdata[i], np.ndarray):  # if the data is an array
                TX_long_data(TXdata[i], dst_add, dev_add, max_length, d)  # transmits the data

            else:  # if the data is a string
                TX_long_data_bytes(TXdata[i], dst_add, dev_add, max_length, d)  # transmits the data

            d.setModeRX()  # sets mode to Rx

            if interruption(.2, d) is True:

                RXdata = receiving_long_split_data_timed(dev_add, .2, d)  # receiving data and concatenating it

                if RXdata is not None:
                    commands = np.frombuffer(RXdata, dtype=control_dtype)

                    for j in range(len(commands)):   # this is to be adjusted according to actual need (this gives drone instructions)
                        task = tuple(commands[j]).index(1)
                        if task == 0:
                            print 'move left'
                        if task == 1:
                            print 'move right'
                        if task == 2:
                            print 'move up'
                        if task == 3:
                            print 'move down'
                        if task == 4:
                            print 'Severing data link'
                            ON = 0
                            break

            if ON == 0:
                break

            drone(TXdata, dst_add, dev_add, max_length, d, i+1)  # transmits the next piece of data

        except IndexError:
            print 'waiting for data update'


# ==== GROUND STATION ====

def ground_station(TXdata, dst_add, dev_add, max_packet_len, d):
    i = 0
    while True:
        print 'waiting for transmission'
        d.setModeRX()  # set mode to Rx

        RXdata = receiving_long_split_data(dev_add, d)  # receiving data and concatenating it

        if RXdata is not None:
            try:
                print np.frombuffer(RXdata, dtype=my_dtype)  # printing the data here (see what is to be done with received data)
            except ValueError:  # data is in the form of a string (implying image in this case)
                i += 1
                image = base64.b64decode(RXdata)
                filename = 'image{}.jpg'.format(i)
                with open(filename, 'wb') as f:
                    f.write(image)

        if len(TXdata) != 0:  # if the GS has something to transmit
            time.sleep(0.1)
            d.RFxmit('INT'.ljust(50,'1'))
            print 'sent interruption'
            d.setModeRX()

            confirmation = RX_timer_return(1, d) # listen out for confirmation for 1 second

            if confirmation is None:
                print 'no acknowledgement; aborting interruption'

            elif 'ACK' in confirmation:
                print 'acknowledgement received'
                time.sleep(0.1)
                d.RFxmit('ACK'.ljust(50,'1'))
                print 'sent acknowledgement'
                time.sleep(0.1)
                TX_long_data(TXdata, dst_add, dev_add, max_packet_len, d)  # send out gs data here (to adjust according to data to be sent)

            else:
                pass

        d.setModeIDLE()
