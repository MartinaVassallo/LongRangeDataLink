from rflib import *

# ==== Configuring YS1 =====

d = RfCat()
d.setModeIDLE()
d.setFreq(433920000)
d.setMdmModulation(MOD_MSK)
d.makePktVLEN(255)
d.setMdmDRate(25000)
# d.setMdmChanSpc(200000)
# d.setEnableMdmFEC(False)

d.setMdmSyncMode(1)
d.setMdmSyncWord(0xcccc)

d.calculateMdmDeviatn()
d.calculatePktChanBW()

d.setPower(0xc0)

# TX_dev = 8000  # deviation to use for Tx
# RX_dev = d.getMdmDeviatn() # deviation to use for Rx
# RX_dev = 5000
# print RX_dev

d.setPktAddr(123)  # address
d.setEnablePktCRC()  # enable CRC

# address check (0x40: no chk , 0x41: chk)
d.getRadioConfig()
rc = d.radiocfg
rc.pktctrl1 = 0x40
d.setRadioConfig()

# d.printRadioConfig()
