from rflib import *

# ==== Configuring YS1 =====

d = RfCat()
d.setModeIDLE()
d.setFreq(433920000)
d.setMdmModulation(MOD_MSK)
d.makePktVLEN(255)
d.setMdmDRate(25000)

d.setMdmSyncMode(1)
d.setMdmSyncWord(0xcccc)

d.setPower(0xc0)

d.setPktAddr(123)  # address
d.setEnablePktCRC()  # enable CRC

# address check (0x40: no chk , 0x41: chk)
d.getRadioConfig()
rc = d.radiocfg
rc.pktctrl1 = 0x40
d.setRadioConfig()

# d.printRadioConfig()
