import serial
import serial.tools.list_ports
import io

class SlaveComm:

    def setPort(self, serial_port):
        self.ser.port = serial_port
        print("Serial set: " + self.ser.port)


    def setBaut(self, baud):
        self.ser.baudrate = baud

    def openConnection(self):
        print("~ ~ ~ ~ ~")
        print("* Opening connection to "+ self.ser.port)
        
        try:
            self.ser.open()
                    
        except serial.serialutil.SerialException:
            self.assumed_connection_status = False
            print("Error: device connection failed")
            print("~ ~ ~ ~ ~")

        else:
            self.assumed_connection_status = True
            self.ser.flush()
            print("* Device connected succesfully")
            print("~ ~ ~ ~ ~")
        print(" ")

    def closeConnection(self):
        print("~ ~ ~ ~ ~")
        print("* Closing connection to "+ self.ser.port)

        try:
            self.ser.close()
            
        except serial.serialutil.SerialException:
            if self.assumed_connection_status:
                print("Error: failed closing "+ self.ser.port)
                print("~ ~ ~ ~ ~")
            else:
                print("Error: device disconnected with errors")
                print("~ ~ ~ ~ ~")
                
        else:
            self.assumed_connection_status = False
            print("* Device disconnected succesfully")
            print("~ ~ ~ ~ ~")
        print(" ")



    def writeString(self, output_string):
        tmp = output_string + b'\n'
        if not self.assumed_connection_status:
            self.openConnection()
        
        if self.assumed_connection_status:
            print("> " + tmp)

            try:
                self.sio.write(str(tmp))
                self.sio.flush()
                
            except serial.serialutil.SerialException:
                self.closeConnection()

        return output_string
                
                
    def writeCommand(self, command="help", parameters=[]):
        tmp = command + "("

        for n in range(0,len(parameters)):
            tmp = tmp +parameters[n]
            if n<len(parameters)-1:
                tmp= tmp +","
            else:
                tmp=tmp+")"
        
        return self.writeString(tmp)

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
                print("< " + str(tmp) )
                return str(tmp)
        else:
            return "-1"

    def getStatus(self):
        return self.assumed_connection_status   

    def scan_ports(self):
        self.portscan = serial.tools.list_ports.comports();
        self.devices = []
        for n in range(len(self.portscan)):
            self.devices.append(self.portscan[n].device)
        print("> Available ports/devices:   ", self.devices)

    def get_ports(self):
        self.scan_ports();
        return self.devices

    def __init__(self, serial_port, baud):
        self.ser = serial.Serial(timeout = 1)
        self.ser.baudrate = baud
        self.ser.port = serial_port
        self.sio = io.TextIOWrapper(    buffer = io.BufferedRWPair(self.ser, self.ser),newline = '\n')
        self.assumed_connection_status = False
        self.devices = []

        self.scan_ports()
        if serial_port != "":
            self.openConnection()