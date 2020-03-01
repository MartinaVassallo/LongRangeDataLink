from rflib import *

# ==== Configuring YS1 =====

d = RfCat()
d.setModeIDLE()
d.setFreq(433920000)
d.setMdmModulation(MOD_MSK)  # Modulation
d.makePktVLEN(255)      # Maximum possible transmission length set
d.setMdmDRate(25000)

d.setMdmSyncMode(1)
d.setMdmSyncWord(0xcccc)

d.calculatePktChanBW()

d.setPower(0xc0) # 0xc0 = 10 mW, 0x60 = 1 mW

d.setEnablePktCRC()  # enable CRC


