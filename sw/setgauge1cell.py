#!/usr/bin/python

# Setuup of LION1CELL MLAB module

import time
import sys
from pymlab import config


if len(sys.argv)!=3:
    sys.stderr.write("Invalid number of arguments.\n")
    sys.stderr.write("Usage: %s #I2CPORT battery_type[NCR18650B|INR18650MJ1] \n" % (sys.argv[0], ))
    sys.exit(1)

port = eval(sys.argv[1])

while True:
    #### Sensor Configuration ###########################################
    cfg = config.Config(
        i2c = {
            "port": port, # I2C bus number
            "device": "hid",
        },

	    bus = [
		    {
                "type": "i2chub",
                "address": 0x73,

                "children": [
                    {"name": "guage", "type": "lioncell", "channel": 7, },
                ],
		    },
	    ],
    )


    cfg.initialize()
    guage = cfg.get_device("guage")

    if "NCR18650B" == sys.argv[2]:
        print("Setting parameters for NCR18650B batteries")
        guage.WriteFlashByte(48, 0, 21, 0x0D)    # Design Capacity 3350 mAh
        guage.WriteFlashByte(48, 0, 22, 0x16)    #
        print("Design Capacity")
        guage.WriteFlashByte(48, 0, 23, 0x2F)    # Design Energy 12177 mWh
        guage.WriteFlashByte(48, 0, 24, 0x91)    #
        print("Design Energy")
        #guage.WriteFlashByte(64, 0, 0, 0x9)      # External Voltage Measurement
        #print "External Voltage Measurement"
        #guage.WriteFlashByte(64, 0, 7, 0x2)      # Two Cells
        #print "Two Cells"
        guage.WriteFlashByte(64, 0, 4, 0x64)     # 7 LED (1+6), Shift Register
        print("LED")
        #guage.WriteFlashByte(104, 0, 14, 0x28)   # Voltage Measurement Range 10240 mV
        #guage.WriteFlashByte(104, 0, 15, 0x00)   #
        #print "Voltage Measurement Range"
        guage.WriteFlashByte(82, 0, 0, 0x0D)     # Set initial cell capacity 3350 mAh
        guage.WriteFlashByte(82, 0, 1, 0x16)     #
        print("Initial cell capacity")
        guage.WriteFlashByte(83, 0, 0, 0x20)     # Set Chem ID
        guage.WriteFlashByte(83, 0, 1, 0x17)     #
        print("Chem ID")
        guage.reset()                            # Reset Guage
        print("Reset")
        time.sleep(1)

    elif "INR18650MJ1" == sys.argv[2]:
        print("Setting parameters for INR18650MJ1 batteries")
        guage.WriteFlashByte(48, 0, 21, 0x0D)    # Design Capacity 3500 mAh
        guage.WriteFlashByte(48, 0, 22, 0xAC)    #
        print("Design Capacity")
        guage.WriteFlashByte(48, 0, 23, 0x31)    # Design Energy 12600 mWh
        guage.WriteFlashByte(48, 0, 24, 0x38)    #
        print("Design Energy")
        #guage.WriteFlashByte(64, 0, 0, 0x9)      # External Voltage Measurement
        #print("External Voltage Measurement")
        #guage.WriteFlashByte(64, 0, 7, 0x2)      # Two Cells
        #print("Two Cells")
        guage.WriteFlashByte(64, 0, 4, 0x64)     # 7 LED (1+6), Shift Register
        print("LED")
        #guage.WriteFlashByte(104, 0, 14, 0x25)   # Voltage Measurement Range 9484 mV
        #guage.WriteFlashByte(104, 0, 15, 0x0C)   #
        #print("Voltage Measurement Range")
        guage.WriteFlashByte(82, 0, 0, 0x0D)     # Set initial cell capacity 3500 mAh
        guage.WriteFlashByte(82, 0, 1, 0xAC)     #
        print("Initial cell capacity")
        guage.WriteFlashByte(83, 0, 0, 0x20)     # Set Chem ID
        guage.WriteFlashByte(83, 0, 1, 0x59)     #
        print("Chem ID")
        guage.reset()                            # Reset Guage
        print("Reset")
        time.sleep(1)

    else:
        print("Uknown battery type requested.")
        sys.exit(0)


    flash = guage.ReadFlashBlock(48, 0)
    print("48 - ")
    print(" ".join([hex(i) for i in flash]))
    flash = guage.ReadFlashBlock(64, 0)
    print("64 - ")
    print(" ".join([hex(i) for i in flash]))
    flash = guage.ReadFlashBlock(104, 0)
    print("104 - ")
    print(" ".join([hex(i) for i in flash]))

    print("DesCap =", guage.DesignCapacity(), "mAh")
    flash = guage.Chemistry()
    print("Chemistry = ")
    print(" ".join([hex(i) for i in flash]))

    try:
        while True:
            # Battery status readout
            print("NominalAvailableCapacity =", guage.NominalAvailableCapacity(), "mAh, FullAvailabeCapacity =", guage.FullAvailabeCapacity(), "mAh, AvailableEnergy =", guage.AvailableEnergy(), "* 10 mWh")
            print("Temp =", guage.getTemp(), "degC, RemainCapacity =", guage.getRemainingCapacity(), "mAh, cap =", guage.FullChargeCapacity(), "mAh, U =", guage.Voltage(), "mV, I =", guage.AverageCurrent(), "mA, charge =", guage.StateOfCharge(), "%")
            time.sleep(3)

    except IOError:
        err = err + 1
        print("IOError")
        continue

    except KeyboardInterrupt:
    	sys.exit(0)
