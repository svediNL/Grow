import matplotlib 
from matplotlib import pyplot as pp
import matplotlib.animation as animation
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

import numpy as np

from ttk import *
try:
    from Tkinter import *
except:
    print("using tkinter")
    from tkinter import *
else:
    print("using Tkinter")

from comms import SlaveComm

import time

BG_MAIN = '#7A7A7A'
BG_SUB = '#B0B0B0'
BG_SUBSUB = '#DDDDDD'


# create app of type Frame
class App( Frame ):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.serial_var_port = StringVar()
        self.serial_var_port.set("/dev/ttyACM0")
        self.arduino = SlaveComm("/dev/ttyACM0", 115200)
        self.serial_var_string = StringVar()

        self.pump_enable = False
        self.pump_state = StringVar()
        self.pump_state.set("pump stopped...")

        self.lamp_enable = False
        self.lamp_state = StringVar()
        self.lamp_state.set("Lamp is off...")

        self.str_time = StringVar()
        self.str_time.set(".....")

        self.create_widgets()

    def disable_lamp(self):
        self.lamp_enable = False
        self.lamp_state.set("Lamp is off...")
        self.arduino.writeCommand("ENABLE_LAMP", ["0"])

    def enable_lamp(self):
        self.lamp_enable = True
        self.lamp_state.set("Lamp is on...")
        self.arduino.writeCommand("ENABLE_LAMP", ["1"])

    def update_lampR(self, value):
        
        #print(value)
        self.arduino.writeCommand("SET_LAMP", ["R", str(int(float(value)))])
        #Set value on arduino
        
    def update_lampG(self, value):
        
        #print(value)
        self.arduino.writeCommand("SET_LAMP", ["G", str(int(float(value)))])
        #Set value on arduino
        
    def update_lampB(self, value):
        
        #print(value)
        self.arduino.writeCommand("SET_LAMP", ["B", str(int(float(value)))])
        #Set value on arduino

    def update_lampW(self, value):
        
        #print(value)
        self.arduino.writeCommand("SET_LAMP", ["W", str(int(float(value)))])

    def update_pump(self, value):
        self.arduino.writeCommand("SET_PUMP", [str(int(float(value))), str(int(self.pump_enable))])

    def set_pumpEnable(self):
        self.pump_enable = not self.pump_enable
        #print(self.pump_enable)
        self.arduino.writeCommand("ENABLE_PUMP", [str(int(self.pump_enable))])

        if self.pump_enable:
            self.pump_state.set("pump running...")
        else:
            self.pump_state.set("pump stopped...")

    def open_serial_connection(self):
        self.arduino.setPort(self.serial_var_port.get())
        self.arduino.openConnection()

    def close_serial_connection(self):
        self.arduino.closeConnection()

    def send_serial_string(self):
        self.arduino.writeString(self.serial_var_string.get())
        self.serial_var_string.set("")

    def create_widgets(self):
        #  C R E A T E   F R A M E S
        # main frames
        self.mainframe = Frame(self, width=2524, height=512 )
        self.mainframe.pack()

        self.headerFrame=Frame(self.mainframe, height = 128, bd=2, relief = SUNKEN)
        self.headerFrame.pack(fill = X, side = TOP)

        self.contentFrame=Frame(self.mainframe, bd=2, relief = SUNKEN)
        self.contentFrame.pack(fill = BOTH, side = BOTTOM)

        self.plotFrame = Frame(self.contentFrame, width = 1280, bd=1, relief = SUNKEN)
        self.plotFrame.pack(fill = Y, side = LEFT)

        self.dicoFrame = Frame(self.contentFrame, bd=1, relief = SUNKEN)
        self.dicoFrame.pack(fill = Y, side = RIGHT)


        #frame for arduino connection
        self.serial_frame = Frame(self.dicoFrame, bd=1, relief = SUNKEN)
        self.serial_frame.pack(fill = X, side = TOP)

        self.serial_notebook = Notebook(self.serial_frame)
        self.serial_connectionFrame = Frame(self.serial_notebook)
        self.serial_interfaceFrame = Frame(self.serial_notebook)

        self.serial_notebook.add(self.serial_connectionFrame, text = 'connect')
        self.serial_notebook.add(self.serial_interfaceFrame, text = 'comm')

        # frame for direct control
        self.devco_frame = Frame(self.dicoFrame , bd=1, relief = SUNKEN)
        self.devco_frame.pack(fill = X, side = TOP)

        self.devco_notebook = Notebook(self.devco_frame)
        self.devco_lamp_frame = Frame(self.devco_notebook)
        self.devco_hydro_frame = Frame(self.devco_notebook)

        self.devco_notebook.add(self.devco_lamp_frame, text = 'LIGHT')
        self.devco_notebook.add(self.devco_hydro_frame, text = 'HYDROLICS')

        #  C R E A T E   W I D G E T S
        # DEVCO
        self.devco_label = Label(self.devco_frame, text= " ~ DEVICE CONTROL  ")
        # create widgets for RGBW light
        # RGBW sliders
        self.devco_slider_white = Scale(self.devco_lamp_frame, orient= HORIZONTAL, command= self.update_lampW, to = 255)
        self.devco_slider_red = Scale(self.devco_lamp_frame, orient= HORIZONTAL, command= self.update_lampR, to = 255)
        self.devco_slider_green = Scale(self.devco_lamp_frame, orient= HORIZONTAL, command= self.update_lampG, to = 255)
        self.devco_slider_blue = Scale(self.devco_lamp_frame, orient= HORIZONTAL, command= self.update_lampB, to = 255)

        # label for RGBW slider
        self.devco_label_white = Label(self.devco_lamp_frame, text= "White:")
        self.devco_label_red = Label(self.devco_lamp_frame, text= "Red:")
        self.devco_label_green = Label(self.devco_lamp_frame, text= "Green:")
        self.devco_label_blue = Label(self.devco_lamp_frame, text= "Blue:")

        self.devco_button_lampOn = Button(self.devco_lamp_frame, text= "ON", command = self.enable_lamp)
        self.devco_button_lampOff = Button(self.devco_lamp_frame, text= "OFF", command = self.disable_lamp)
        self.devco_label_lampState = Label(self.devco_lamp_frame, textvariable = self.lamp_state)


        # create widgets for pump control
        self.devco_slider_pumpValue = Scale(self.devco_hydro_frame, orient= HORIZONTAL, command= self.update_pump, to = 255)
        self.devco_button_pumpEnable = Button(self.devco_hydro_frame, command = self.set_pumpEnable, text = "toggle pump")
        self.devco_label_pumpRunning = Label(self.devco_hydro_frame, textvariable = self.pump_state)

        # SERIAL
        # create widgets for serial connection
        self.serial_entry_port = Entry(self.serial_connectionFrame, textvariable= self.serial_var_port)
        self.serial_button_open= Button(self.serial_connectionFrame, text = "open", command= self.open_serial_connection)
        self.serial_button_close = Button(self.serial_connectionFrame,text = "close", command= self.close_serial_connection)

        self.serial_entry_command = Entry(self.serial_interfaceFrame, textvariable= self.serial_var_string)
        self.serial_button_send= Button(self.serial_interfaceFrame, text = "send", command= self.send_serial_string)


        # header texts
        self.label_header = Label(self.headerFrame, text= "                    +-~-~-~-~-~-+ Grow Controller +-~-~-~-~-~-+ ")
        self.label_time = Label(self.headerFrame, textvariable = self.str_time)
        

        #  W I D G E T   L A Y O U T
        # header texta
        # serial conneciton
        self.serial_entry_port.grid(row= 0, column=0, columnspan=2)
        self.serial_button_close.grid(row=1, column=0)
        self.serial_button_open.grid(row=1,column=1)

        self.serial_entry_command.grid(row = 0 , column = 0, columnspan = 2)
        self.serial_button_send.grid(row = 1 , column = 0)

        self.serial_notebook.grid(row=0, column =0, sticky= N)

        # RGBW lamp
        self.devco_label.grid(row= 0 , column = 0, sticky= W)
        self.devco_button_lampOff.grid   (row=0, column= 0)
        self.devco_button_lampOn.grid    (row=0, column= 2)
        self.devco_label_lampState.grid  (row=1, column=0, columnspan=3)

        self.devco_label_white.grid  (row = 2, column = 0, sticky= SW )
        self.devco_label_red.grid    (row = 3, column = 0, sticky= SW )
        self.devco_label_green.grid  (row = 4, column = 0, sticky= SW )
        self.devco_label_blue.grid   (row = 5, column = 0, sticky= SW )
        self.devco_slider_white.grid (row = 2, column = 1, columnspan = 2, sticky = NW )
        self.devco_slider_red.grid   (row = 3, column = 1, columnspan = 2, sticky = NW )
        self.devco_slider_green.grid (row = 4, column = 1, columnspan = 2, sticky = NW )
        self.devco_slider_blue.grid  (row = 5, column = 1, columnspan = 2, sticky = NW )


        # pump interface
        self.devco_slider_pumpValue.grid(row = 0, column = 0)
        self.devco_button_pumpEnable.grid(row = 2, column = 0)
        self.devco_label_pumpRunning.grid(row=1, column =0, sticky= S)

        
        self.devco_notebook.grid(row = 1, column = 0, sticky= N)

        self.label_header.grid(row = 0, column = 0, sticky = W)
        self.label_time.grid(row = 0, column = 1, sticky = E)     

        self.pack()

        self.plot_canvas = FigureCanvasTkAgg(f, self.plotFrame)
        self.plot_canvas.show()
        self.plot_canvas.get_tk_widget().grid(row = 0, column = 0)

# prepare animation buffer
BUFF_LEN = 4096
BUFF_FILL = 0
valM = np.zeros( shape=(2,BUFF_LEN) )
valH = np.zeros( shape=(2,BUFF_LEN) )

for n in range(BUFF_LEN):
    valM[0,n]=n*-0.5;
    valH[0,n]=n*-0.5;

# define animation and call read command
def animate(i):
    global BUFF_FILL, valM, valH

    # shift values
    for n in reversed(range( 1, BUFF_LEN )):
        valM[1,n]= valM[1,n-1]
        valH[1,n]= valH[1,n-1]

    # add new value
    valM[1,0] = app.arduino.readCommand("GET_MOISTURE")
    print(valM[1,0])
    #valM[1,0] = valM[1,0] + 1

    valH[1,0] = app.arduino.readCommand("GET_TEMP")
    print(valH[1,0])
    #valH[1,0] = (valH[1,0]+1) % 2

    # reverse value array for neatness
    valMneat = np.flip(valM, 1)
    valHneat = np.flip(valH, 1)

    # do plot stuff
    if BUFF_FILL < BUFF_LEN:
        BUFF_FILL = BUFF_FILL + 1

#    UPDATE MOUSTURE PLOT
    moistPlot.clear()
    
    moistPlot.set_ylim([0,100])
    moistPlot.set_ylabel("% of FSV [%]")
    moistPlot.set_xlabel("time [min]")
    moistPlot.grid(True)    
    moistPlot.plot( valMneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valMneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )
    
    
#   UPDATE TEMOERATURE PLOT
    heatPlot.clear()
    
    heatPlot.set_ylim([ min(10, min(valHneat[0 , BUFF_LEN-BUFF_FILL:BUFF_LEN])), 
                        max(40, max(valHneat[0, BUFF_LEN-BUFF_FILL : BUFF_LEN])) ])
    heatPlot.set_ylabel("temp [*C]")
    heatPlot.set_xlabel("time [min]")
    heatPlot.grid(True)
    
    heatPlot.plot( valHneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valHneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )
    # print(BUFF_FILL)

#  A D D   P L O T
f = pp.Figure(figsize=(6,8),dpi = 100)

moistPlot = f.add_subplot(211)
moistPlot.set_ylim([0,100])
moistPlot.set_ylabel("% of FSV [%]")
moistPlot.set_xlabel("time [min]")
moistPlot.grid(True)
    
heatPlot = f.add_subplot(212)
heatPlot.set_ylim([10,40])
heatPlot.set_ylabel("temp [*C]")
heatPlot.set_xlabel("time [min]")

heatPlot.grid(True)

#moistPlot.plot(valM[0,:], valM[1,:])
#heatPlot.plot(valH[0,:], valH[1,:])
moistPlot.plot(0, 0)
heatPlot.plot(0, 0)


#run app
root = Tk() #init Tk
app = App(master=root)  # assign tk to master frame

def program():
    eptime = time.time()
    struct_time = time.localtime(eptime)
    struct_time_str = str(struct_time.tm_hour) + " : " + str(struct_time.tm_min) + " : " + str(struct_time.tm_sec)

    print eptime
    print struct_time_str 
    app.str_time.set(struct_time_str)

    root.after(10000, program)
root.after(10000, program)

ani = animation.FuncAnimation(f, animate, interval = 30000)
app.mainloop()
app.arduino.closeConnection()
sys.exit()
