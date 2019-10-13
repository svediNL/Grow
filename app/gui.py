import matplotlib 
from matplotlib import pyplot as pp
import matplotlib.animation as animation
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

import numpy as np

try:
    from Tkinter import *
except:
    from tkinter import *

from ttk import *
from comms import SlaveComm

# create app of type Frame
class App( Frame ):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.serial_var_port = StringVar()
        self.serial_var_port.set("/dev/ttyACM0")
        self.arduino = SlaveComm("/dev/ttyACM0", 115200)

        self.pump_enable = False
        self.pump_state = StringVar()
        self.pump_state.set("pump stopped...")

        self.lamp_enable = False
        self.lamp_state = StringVar()
        self.lamp_state.set("Lamp is off...")

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
        
        print(value)
        self.arduino.writeCommand("SET_LAMP", ["R", str(int(float(value)))])
        #Set value on arduino
        
    def update_lampG(self, value):
        
        print(value)
        self.arduino.writeCommand("SET_LAMP", ["G", str(int(float(value)))])
        #Set value on arduino
        
    def update_lampB(self, value):
        
        print(value)
        self.arduino.writeCommand("SET_LAMP", ["B", str(int(float(value)))])
        #Set value on arduino

    def update_lampW(self, value):
        
        print(value)
        self.arduino.writeCommand("SET_LAMP", ["W", str(int(float(value)))])

    def update_pump(self, value):
        self.arduino.writeCommand("SET_PUMP", [str(int(float(value))), str(int(self.pump_enable))])

    def set_pumpEnable(self):
        self.pump_enable = not self.pump_enable
        print(self.pump_enable)
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

    def create_widgets(self):

        #  C R E A T E   F R A M E S
        # main frames
        self.topFrame=Frame(self)
        self.leftFrame = Frame(self)
        self.rightFrame = Frame(self)

        #frame for arduino connection
        self.serial_frame = Frame(self.topFrame)

        # frame for direct control
        self.dico_notebook = Notebook(self.rightFrame)
        self.dico_lamp_frame = Frame(self.dico_notebook)
        self.dico_hydro_frame = Frame(self.dico_notebook)

        self.dico_notebook.add(self.dico_lamp_frame, text = 'LIGHT')
        self.dico_notebook.add(self.dico_hydro_frame, text = 'HYDROLICS')


        #  C R E A T E   W I D G E T S
        # header texts
        self.label_header = Label(self.topFrame, text= " +-~-~-~-~-~-+ Grow Controller +-~-~-~-~-~-+ ")
        self.label_dico = Label(self.rightFrame, text= " DIRECT CONTROL ")

        # create widgets for RGBW light
        # RGBW sliders
        self.dico_slider_white = Scale(self.dico_lamp_frame, orient= HORIZONTAL, command= self.update_lampW, to = 255)
        self.dico_slider_red = Scale(self.dico_lamp_frame, orient= HORIZONTAL, command= self.update_lampR, to = 255)
        self.dico_slider_green = Scale(self.dico_lamp_frame, orient= HORIZONTAL, command= self.update_lampG, to = 255)
        self.dico_slider_blue = Scale(self.dico_lamp_frame, orient= HORIZONTAL, command= self.update_lampB, to = 255)
        # label for RGBW slider
        self.dico_label_white = Label(self.dico_lamp_frame, text= "White:")
        self.dico_label_red = Label(self.dico_lamp_frame, text= "Red:")
        self.dico_label_green = Label(self.dico_lamp_frame, text= "Green:")
        self.dico_label_blue = Label(self.dico_lamp_frame, text= "Blue:")

        self.dico_button_lampOn = Button(self.dico_lamp_frame, text= "ON", command = self.enable_lamp)
        self.dico_button_lampOff = Button(self.dico_lamp_frame, text= "OFF", command = self.disable_lamp)
        self.dico_label_lampState = Label(self.dico_lamp_frame, textvariable = self.lamp_state)

        # create widgets for pump control
        self.dico_slider_pumpValue = Scale(self.dico_hydro_frame, orient= HORIZONTAL, command= self.update_pump, to = 255)
        self.dico_button_pumpEnable = Button(self.dico_hydro_frame, command = self.set_pumpEnable, text = "toggle pump")
        self.dico_label_pumpRunning = Label(self.dico_hydro_frame, textvariable = self.pump_state)

        # create widgets for serial connection
        self.serial_entry_port = Entry(self.serial_frame, textvariable= self.serial_var_port)
        self.serial_button_open= Button(self.serial_frame, text = "open", command= self.open_serial_connection)
        self.serial_button_close = Button(self.serial_frame,text = "close", command= self.close_serial_connection)

        #  W I D G E T   L A Y O U T
        # header texta
        self.label_header.grid(row = 0, column = 0, columnspan = 2 )
        self.label_dico.grid(row= 0 , column = 0, sticky= N)

        # serial conneciton
        self.serial_entry_port.grid(row= 0, column=0, columnspan=2)
        self.serial_button_close.grid(row=1, column=0)
        self.serial_button_open.grid(row=1,column=1)

        # RGBW lamp
        self.dico_button_lampOff.grid   (row=0, column= 0)
        self.dico_button_lampOn.grid    (row=0, column= 2)
        self.dico_label_lampState.grid  (row=1, column=0, columnspan=3)

        self.dico_label_white.grid  (row = 2, column = 0, sticky= SW )
        self.dico_label_red.grid    (row = 3, column = 0, sticky= SW )
        self.dico_label_green.grid  (row = 4, column = 0, sticky= SW )
        self.dico_label_blue.grid   (row = 5, column = 0, sticky= SW )
        self.dico_slider_white.grid (row = 2, column = 1, columnspan = 2, sticky = NW )
        self.dico_slider_red.grid   (row = 3, column = 1, columnspan = 2, sticky = NW )
        self.dico_slider_green.grid (row = 4, column = 1, columnspan = 2, sticky = NW )
        self.dico_slider_blue.grid  (row = 5, column = 1, columnspan = 2, sticky = NW )


        # pump interface
        self.dico_slider_pumpValue.grid(row = 0, column = 0)
        self.dico_button_pumpEnable.grid(row = 2, column = 0)
        self.dico_label_pumpRunning.grid(row=1, column =0, sticky= S)

        #  F R A M E   L A Y O U T
        self.topFrame.grid(row = 0, column = 0, columnspan = 2)
        self.leftFrame.grid(row=1, column=0)
        self.rightFrame.grid(row=1, column=1)
        self.serial_frame.grid(row=1, column=0, sticky= W)
        self.dico_notebook.grid(row = 1, column = 0, sticky= N)

        self.pack()

        self.plot_canvas = FigureCanvasTkAgg(f, self.leftFrame)
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
    
    moistPlot.set_ylim([0,1024])
    moistPlot.set_ylabel("analog input byte [0-1023]")
    moistPlot.set_xlabel("time [min]")
    moistPlot.grid(True)    
    moistPlot.plot( valMneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valMneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )
    
    
#   UPDATE TEMOERATURE PLOT
    heatPlot.clear()
    
    heatPlot.set_ylim([10,40])
    heatPlot.set_ylabel("temp [*C]")
    heatPlot.set_xlabel("time [min]")
    heatPlot.grid(True)
    
    heatPlot.plot( valHneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valHneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

    # print(BUFF_FILL)

#  A D D   P L O T
f = pp.Figure(figsize=(10,5),dpi = 100)

moistPlot = f.add_subplot(121)
moistPlot.set_ylim([0,1024])
moistPlot.set_ylabel("analog input byte [0-1023]")
moistPlot.set_xlabel("time [min]")
moistPlot.grid(True)
    
heatPlot = f.add_subplot(122)
heatPlot.set_ylim([10,40])
heatPlot.set_ylabel("temp [*C]")
heatPlot.set_xlabel("time [min]")

heatPlot.grid(True)

moistPlot.plot(valM[0,:], valM[1,:])
heatPlot.plot(valH[0,:], valH[1,:])

#run app
root = Tk() #init Tk
app = App(master=root)  # assign tk to master frame
ani = animation.FuncAnimation(f, animate, interval = 30000)
app.mainloop()
app.arduino.closeConnection()
sys.exit()
