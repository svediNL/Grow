import RPi.GPIO as GPIO
import datetime, sys
from comms import SlaveComm

slave= SlaveComm("/dev/ttyUSB0", 9600)

runbool = True
lightOutput = False

while runbool:
    try:
        cTime = datetime.datetime.now()
        if cTime.second % 2 == 0:
            slave.write("GET_MOISTURE")
            
            #(cTime.second)
            if cTime.second <= 30 and not lightOutput:
                slave.write("SET_LIGHT:1")
                print("under")
                lightOutput = True
            elif cTime.second > 30 and lightOutput:
                slave.write("SET_LIGHT:0")
                slave.sio.flush()
                print("over")
                lightOutput = False
    except KeyboardInterrupt:
        slave.ser.close()
        GPIO.cleanup()
        sys.exit()
        #runbool = False
