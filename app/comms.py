import serial
import io

class SlaveComm:

    def setPort(self, serial_port):
        self.ser.port = serial_port
        print("Serial set: " + self.ser.port)


    def setBaut(self, baud):
        self.ser.baudrate = baud

    def openConnection(self):
        print("o - o - o")
        print("opening connection to "+ self.ser.port)
        
        try:
            self.ser.open()
                    
        except serial.serialutil.SerialException:
            self.assumed_connection_status = False
            print("device connection failed")
            print("x - x - x")

        else:
            self.assumed_connection_status = True
            self.ser.flush()
            print("device connected")
            print("o - o - o")

    def closeConnection(self):
        # print("x - x - x")
        # print("closing connection to "+ self.ser.port)

        try:
            self.ser.close()
            
        except serial.serialutil.SerialException:
            if self.assumed_connection_status:
                print("failed closing "+ self.ser.port)
                print("o - o - o")
            else:
                print("device disconnected with errors")
                print("x - x - x")
                
        else:
            self.assumed_connection_status = False
            # print("device succesfully disconnected")
            # print("x - x - x")



    def writeString(self, output_string):
        if not self.assumed_connection_status:
            self.openConnection()
        
        print "> " + output_string
        if self.assumed_connection_status:
            tmp = output_string + "\n"
            try:
                self.sio.write(unicode(tmp))
                self.sio.flush()
                
            except serial.serialutil.SerialException:
                self.closeConnection()
                
                
    def writeCommand(self, command="help", parameters=[]):
        tmp = command + "("

        for n in range(0,len(parameters)):
            tmp = tmp +parameters[n]
            if n<len(parameters)-1:
                tmp= tmp +","
            else:
                tmp=tmp+")"
        
        self.writeString(tmp)

    def readCommand(self, command= "help", parameters= []):
        if self.assumed_connection_status:
            self.ser.reset_input_buffer() # clear input
            tmp = b''   # set tmp type
            self.writeCommand(command, parameters)  # write read-command and wait for answer

            try:
                tmp = self.ser.read_until(b'@')
                tmp = tmp[:-1]
            except serial.serialutil.SerialException:
                print("communication error")
                return "-1"
            except serial.serialutil.SerialTimeout:
                print("timeout")
                return "-1"
            else:
                print "< " + str(tmp) 
                return str(tmp)
        else:
            return "-1"

    def getStatus(self):
        return self.assumed_connection_status   

    def __init__(self, serial_port, baud):
        self.ser = serial.Serial(timeout = 1)
        self.ser.baudrate = baud
        self.ser.port = serial_port
        self.sio = io.TextIOWrapper(    buffer = io.BufferedRWPair(self.ser, self.ser),newline = '\n')
        self.assumed_connection_status = False
        self.openConnection()