import serial
import io

class SlaveComm:

    def setPort(self, serial_port):
        self.ser.port = serial_port
        print("Serial set: " + self.ser.port)


    def setBaut(self, baud):
        self.ser.baudrate = baud

    def openConnection(self):
        print("opening connection to "+ self.ser.port)
        
        try:
            self.ser.open()
            runbool = True
            while runbool:
                msg = self.ser.read_until(b'\n')
                if msg == b'Running\r\n':
                    runbool = False
                else:
                    print(msg)
                    
        except serial.serialutil.SerialException:
            print("failed opening "+ self.ser.port)
        else:
            print("Slave connected")

    def closeConnection(self):
        self.ser.close()

    def writeString(self, inputString):
        
        if not self.ser.isOpen:
            self.openConnection()
        
        if self.ser.isOpen:
            tmp = inputString + "\n"
            try:
                self.sio.write(unicode(tmp))
                self.sio.flush()
                
            except serial.serialutil.SerialException:
                print("communication error")
                
    def writeCommand(self, command, parameters):
        tmp = command + "("

        for n in range(0,len(parameters)):
            tmp = tmp +parameters[n]
            if n<len(parameters)-1:
                tmp= tmp +","
            else:
                tmp=tmp+")"
        print(tmp)
        
        self.writeString(tmp)

    def readCommand(self, command):

        self.writeCommand(command, [])

        if self.ser.isOpen:
            tmp = b''
            try:
                tmp = self.ser.read_until(b'\n')
                #for n in range()
                try:
                    float(tmp)
                except ValueError:
                    print "value error: "+tmp
                else:
                    return float(tmp)
                
            except serial.serialutil.SerialException:
                print("communication error")

    def __init__(self, serial_port, baud):
        self.ser = serial.Serial()
        self.ser.baudrate = baud
        self.ser.port = serial_port

        self.sio = io.TextIOWrapper( buffer = io.BufferedRWPair(self.ser, self.ser),
                                     newline = '\n')
        
        self.closeConnection()
        self.openConnection()


        

