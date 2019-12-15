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

PROGRAM_CYLCETIME= 1000.0
ANI_CYCLETIME = 5000

NAME_RELAY_1 = "RELAY 1"
NAME_RELAY_2 = "RELAY 2"

# create app of type Frame
class App( Frame ):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.serial_var_port = StringVar()
        self.serial_var_port.set("/dev/ttyACM0")
        self.arduino = SlaveComm("/dev/ttyACM0", 115200)
        self.serial_var_string = StringVar()

        self.serial_connection_string = StringVar()
        if self.arduino.getStatus():
            self.serial_connection_string.set("Connected")
        else:
            self.serial_connection_string.set("Disconnected")

        self.pump_enable = False
        self.pump_state = StringVar()
        self.pump_state.set("pump stopped...")

        self.enable_relay1 = IntVar()
        self.enable_relay2 = IntVar()

        self.lamp_enable = False
        self.lamp_state = StringVar()
        self.lamp_state.set("Lamp is off...")

        self.enable_daylight = IntVar()
        self.daylight_status = StringVar()
        self.daylight_brightness = StringVar()
        self.daylight_tv_start_hour = StringVar()
        self.daylight_tv_start_min = StringVar()
        self.daylight_tv_end_hour = StringVar()
        self.daylight_tv_end_min = StringVar()
        self.daylight_tv_ramp_hour = StringVar()
        self.daylight_tv_ramp_min = StringVar()

        self.daylight_status.set("Daylight disabled")
        self.daylight_brightness.set("255")
        self.daylight_tv_start_hour.set("7")
        self.daylight_tv_start_min.set("00")
        self.daylight_tv_end_hour.set("19")
        self.daylight_tv_end_min.set("00")
        self.daylight_tv_ramp_hour.set("00")
        self.daylight_tv_ramp_min.set("05")

        self.daylight_stepsize = 1.0
        self.daylight_output = 0.0
        self.daybool = False
        self.nightbool = False

        self.str_time = StringVar()
        self.str_time.set(".....")

        self.moisture_var = StringVar()
        self.temperature_var = StringVar()

        self.create_widgets()

    def disable_lamp(self):
        self.lamp_state.set("LAMP DISABLED")
        self.arduino.writeCommand("ENABLE_LAMP", ["0"])

    def enable_lamp(self):
        self.lamp_state.set("LAMP ENABLED")
        self.arduino.writeCommand("ENABLE_LAMP", ["1"])

    def update_lampW(self, value):
        
        #print(value)
        self.arduino.writeCommand("SET_LAMP", ["W", str(int(float(value)))])

    def update_daylight_params(self):
        try:
            if float(self.daylight_tv_ramp_min.get())>0 or float(self.daylight_tv_ramp_hour.get())>0:
                self.daylight_stepsize = float(self.daylight_brightness.get()) / ( ( float(self.daylight_tv_ramp_hour.get())*3600 + float(self.daylight_tv_ramp_min.get())*60 ) / float(PROGRAM_CYLCETIME/1000) )
                print self.daylight_stepsize
        except ValueError:
            print "Value Error"

        return True 
        

    def update_pump(self, value):
        self.arduino.writeCommand("SET_PUMP", [str(int(float(value))), str(int(self.pump_enable))])
        if self.pump_enable:
            self.pump_state.set("pump running...")
        else:
            self.pump_state.set("pump stopped...")

    def set_pumpEnable(self):
        self.pump_enable = True
        self.arduino.writeCommand("ENABLE_PUMP", [str(int(self.pump_enable))])
        self.pump_state.set("pump running...")

    def set_pumpDisable(self):
        self.pump_enable = False
        self.arduino.writeCommand("ENABLE_PUMP", [str(0)])
        self.pump_state.set("pump stopped...")

    def open_serial_connection(self):
        self.arduino.setPort(self.serial_var_port.get())
        self.arduino.openConnection()

        if self.arduino.getStatus():
            self.serial_connection_string.set("Connected")
        else:
            self.serial_connection_string.set("Disconnected")

    def close_serial_connection(self):
        self.arduino.closeConnection()
        if self.arduino.getStatus():
            self.serial_connection_string.set("Connected")
        else:
            self.serial_connection_string.set("Disconnected")

    def write_serial_string(self):
        self.arduino.writeString(self.serial_var_string.get())
        self.serial_var_string.set("")

    def read_serial_string(self):
        self.arduino.readCommand(self.serial_var_string.get())
        self.serial_var_string.set("")

    def toggle_relay1(self):
        if self.enable_relay1.get() == 0:
            self.arduino.writeCommand("SET_RELAY", [str(0), str(0)])
        elif self.enable_relay1.get() == 1:
            self.arduino.writeCommand("SET_RELAY", [str(0), str(1)])

    def toggle_relay2(self):
        if self.enable_relay2.get() == 0:
            self.arduino.writeCommand("SET_RELAY", [str(1), str(0)])
        elif self.enable_relay2.get() == 1:
            self.arduino.writeCommand("SET_RELAY", [str(1), str(1)])

    def create_widgets(self):
        # CREATE MAIN FRAME
        self.mainframe = Frame(self)
        self.mainframe.pack()

# H E A D E R   F R A M E
    # CREATE HEADER FRAME
        self.headerFrame=Frame(self.mainframe, height = 128, bd=2, relief = SUNKEN)
        self.headerFrame.pack(fill = BOTH, side = TOP)

    # HEADER TEXT
        self.label_header = Label(self.headerFrame, text= " +- ~ - ~ - ~ - ~ - ~ -+  G R O W   M A S T E R     v1.2  +- ~ - ~ - ~ - ~ - ~ -+ ")
        self.label_header.pack(side = LEFT)

    # CURRENT TIME LABEL
        self.label_time = Label(self.headerFrame, textvariable = self.str_time)
        self.label_time.pack(side = RIGHT)



# C O N T E N T   F R A M E
        self.contentFrame=Frame(self.mainframe, bd=2, relief = SUNKEN)
        self.contentFrame.pack(side = BOTTOM, expand = True)



# D I R E C T   C O N T R O L   F R A M E
        self.dicoFrame = Frame(self.contentFrame, width = 600, bd=1, relief = SUNKEN)
        self.dicoFrame.pack(fill = BOTH, side = RIGHT)


# S E R I A L  F R A M E
        self.serial_frame = Frame(self.dicoFrame, bd=1, relief = SUNKEN)
        self.serial_frame.pack(side = TOP, fill = Y)

    # SERIAL HEADER TEXT
        self.serial_header_label = Label(self.serial_frame, text = "~  S E R I A L ")
        self.serial_header_label.grid(column = 0, row=0, sticky=N+S+W)

    # SERIAL NOTEBOOK
        self.serial_notebook = Notebook(self.serial_frame, width = 300)
        self.serial_notebook.grid(column = 0, row=1, sticky=N+S+E+W)

    # SERIAL NOTEBOOK _ CONNECTIO
        self.serial_connectionFrame = Frame(self.serial_notebook)
        self.serial_notebook.add(self.serial_connectionFrame, text = 'connect')

        self.serial_entry_port = Entry(self.serial_connectionFrame, textvariable= self.serial_var_port)
        self.serial_entry_port.pack(side= TOP, fill = X)

        self.serial_label_status = Label(self.serial_connectionFrame, textvariable = self.serial_connection_string)
        self.serial_label_status.pack(side= TOP, fill = X, expand = True)

        self.serial_button_open= Button(self.serial_connectionFrame, text = "open", command= self.open_serial_connection)
        self.serial_button_open.pack(side= RIGHT, fill = X, expand = True)

        self.serial_button_close = Button(self.serial_connectionFrame,text = "close", command= self.close_serial_connection)
        self.serial_button_close.pack(side = RIGHT, fill = X, expand = True)

    # SERIAL NOTEBOOK _ DIRECT INTERFACE
        self.serial_interfaceFrame = Frame(self.serial_notebook)    
        self.serial_notebook.add(self.serial_interfaceFrame, text = 'comm')

        self.serial_entry_command = Entry(self.serial_interfaceFrame, textvariable= self.serial_var_string)
        self.serial_entry_command.pack(side= TOP, fill = X)

        self.serial_button_read= Button(self.serial_interfaceFrame, text = "read", command= self.read_serial_string)
        self.serial_button_read.pack(side = LEFT, fill = BOTH, expand =True)

        self.serial_button_write= Button(self.serial_interfaceFrame, text = "write", command= self.write_serial_string)
        self.serial_button_write.pack(side = LEFT, fill = BOTH, expand =True)

# L I V E   S T A T U S   F R A M E
        self.live_frame = Frame(self.dicoFrame, bd=1, relief= SUNKEN)
        self.live_frame.grid_columnconfigure(0, weight =1)
        self.live_frame.grid_columnconfigure(1, weight =1)
        self.live_frame.pack(fill = BOTH, side = TOP)

        self.live_label = Label(self.live_frame, text = "~ L I V E   M O N I T O R")
        self.live_label.grid(column = 0, row = 0, columnspan = 2, sticky = N+S+W)

        self.live_moist_label   = Label(self.live_frame, text = "Current moisture: ")
        self.live_moist_label.grid(column = 0, row= 1, sticky=N+S+W)
        self.live_moist_value   = Label(self.live_frame, textvariab = self.moisture_var)
        self.live_moist_value.grid(column = 1, row= 1, sticky=E)

        self.live_heat_label    = Label(self.live_frame, text = "Current temperature: ")
        self.live_heat_label.grid(column = 0, row= 2, sticky=N+S+W)
        self.live_heat_value    = Label(self.live_frame, textvariab = self.temperature_var)
        self.live_heat_value.grid(column = 1, row= 2, sticky=E)

# D E V I C E  C O N T R O L  F R A M E
        self.devco_frame = Frame(self.dicoFrame , bd=1, relief = SUNKEN)
        self.devco_frame.pack(fill = Y, side = TOP)

    # DEVICE CONTROL HEADER TEXT
        self.devco_label = Label(self.devco_frame, text= "~  D E V I C E  C O N T R O L ")
        self.devco_label.grid(column = 0, row=0, sticky=N+S+W)

    # DEVICE CONTROL NOTEBOOL
        self.devco_notebook = Notebook(self.devco_frame, width = 300)
        self.devco_notebook.grid(column = 0, row=1, sticky=N+S+E+W)

    # DEVCO NOTBOOK _ LAMP CONTROL
        self.devco_lamp_frame = Frame(self.devco_notebook)
        self.devco_notebook.add(self.devco_lamp_frame, text = 'LIGHT', sticky=N+S+E+W)

        self.devco_lamp_direct_frame = Frame(self.devco_lamp_frame, bd=2, relief = SUNKEN)
        self.devco_lamp_direct_frame.pack(side = TOP, fill = BOTH)
        self.devco_lamp_direct_frame.grid_columnconfigure(0, weight =1)
        self.devco_lamp_direct_frame.grid_columnconfigure(1, weight =1)
        self.devco_lamp_direct_frame.grid_columnconfigure(2, weight =1)
        self.devco_lamp_direct_frame.grid_columnconfigure(3, weight =1)

        # LAMP STATE
        self.devco_label_lampState = Label(self.devco_lamp_direct_frame, textvariable = self.lamp_state)
        self.devco_label_lampState.grid(column = 0, columnspan = 4, row = 0)

        # SLIDER LABELS
        self.devco_label_white = Label(self.devco_lamp_direct_frame, text= "Raw output:")
        self.devco_label_white.grid(column = 0, row = 1, sticky=S+W)

        # SLIDERS
        self.devco_slider_lamp = Scale(self.devco_lamp_direct_frame, orient= HORIZONTAL, command= self.update_lampW, to = 255)
        self.devco_slider_lamp.grid(column = 1, row = 1, columnspan = 3, sticky=S+W+N+E)

        # ON BUTTON
        self.devco_button_lampOff = Button(self.devco_lamp_direct_frame, text= "OFF", command = self.disable_lamp)
        self.devco_button_lampOff.grid(column = 0, columnspan = 2, row = 2, sticky=N+S+E+W)

        # OFF BUTTON
        self.devco_button_lampOn = Button(self.devco_lamp_direct_frame, text= "ON", command = self.enable_lamp)
        self.devco_button_lampOn.grid(column = 2, columnspan = 2, row = 2, sticky=N+S+E+W)

        # AUTOMATIC LIGHT MODE
        self.devco_lamp_daylight_frame = Frame(self.devco_lamp_frame, bd=2, relief = SUNKEN)
        self.devco_lamp_daylight_frame.pack(side=TOP , fill = BOTH)
        self.devco_lamp_daylight_frame.grid_columnconfigure(0, weight =1)
        self.devco_lamp_daylight_frame.grid_columnconfigure(1, weight =1)
        self.devco_lamp_daylight_frame.grid_columnconfigure(2, weight =1)
        self.devco_lamp_daylight_frame.grid_columnconfigure(3, weight =1)

        self.devco_daylight_toggle = Checkbutton(self.devco_lamp_daylight_frame, text= "Toggle automatic daylight mode", variable = self.enable_daylight, onvalue= 1, offvalue=0, command = self.update_daylight_params)
        self.devco_daylight_toggle.grid(column = 0, row = 1, columnspan = 4, sticky=S+W+N+E)

        self.devco_daylight_status = Label(self.devco_lamp_daylight_frame, textvariable= self.daylight_status)
        self.devco_daylight_status.grid(column = 0, row = 2, columnspan = 4, sticky=S+W+N+E)

        self.devco_daylight_start_label = Label(self.devco_lamp_daylight_frame, text = "Day start")
        self.devco_daylight_start_label.grid(column = 0, row = 3, columnspan = 1, sticky=S+W+N)

        self.devco_daylight_start_hour = Entry(self.devco_lamp_daylight_frame, textvariable = self.daylight_tv_start_hour, width =3)
        self.devco_daylight_start_hour.grid(column = 2, row = 3)

        self.devco_daylight_start_minute = Entry(self.devco_lamp_daylight_frame, textvariable = self.daylight_tv_start_min, width =3)
        self.devco_daylight_start_minute.grid(column = 3, row = 3)

        self.devco_daylight_end_label = Label(self.devco_lamp_daylight_frame, text = "Day end")
        self.devco_daylight_end_label.grid(column = 0, row = 4, columnspan = 1, sticky=S+W+N)

        self.devco_daylight_end_hour = Entry(self.devco_lamp_daylight_frame, textvariable = self.daylight_tv_end_hour, width =3)
        self.devco_daylight_end_hour.grid(column = 2, row = 4)

        self.devco_daylight_end_minute = Entry(self.devco_lamp_daylight_frame, textvariable = self.daylight_tv_end_min, width =3)
        self.devco_daylight_end_minute.grid(column = 3, row = 4)

        self.devco_daylight_ramp_label = Label(self.devco_lamp_daylight_frame, text = "Sunrise/set period")
        self.devco_daylight_ramp_label.grid(column = 0, row = 5, columnspan = 1, sticky=S+W+N)

        self.devco_daylight_ramp_hour = Entry(self.devco_lamp_daylight_frame, textvariable = self.daylight_tv_ramp_hour,validate = "all", validatecommand = self.update_daylight_params, width =3)
        self.devco_daylight_ramp_hour.grid(column = 2, row = 5)

        self.devco_daylight_ramp_minute = Entry(self.devco_lamp_daylight_frame, textvariable = self.daylight_tv_ramp_min,validate = "all", validatecommand = self.update_daylight_params, width =3)
        self.devco_daylight_ramp_minute.grid(column = 3, row = 5)

        self.devco_daylight_brightness_label = Label(self.devco_lamp_daylight_frame, text = "Full brightness")
        self.devco_daylight_brightness_label.grid(column = 0, row = 6, columnspan = 1, sticky=S+W+N)
        self.devco_daylight_brightness_value = Entry(self.devco_lamp_daylight_frame, textvariable = self.daylight_brightness, width =3)
        self.devco_daylight_brightness_value.grid(column = 3, row = 6)


    # DEVCO NOTBOOK _ PUMP CONTROL
        self.devco_hydro_frame = Frame(self.devco_notebook)
        self.devco_hydro_frame.grid_columnconfigure(0, weight =1)
        self.devco_hydro_frame.grid_columnconfigure(1, weight =1)
        self.devco_hydro_frame.grid_columnconfigure(2, weight =1)
        self.devco_hydro_frame.grid_columnconfigure(3, weight =1)
        self.devco_notebook.add(self.devco_hydro_frame, text = 'HYDROLICS', sticky=N+S+E+W)

        # PUMP RUNNING FB
        self.devco_label_pumpRunning = Label(self.devco_hydro_frame, textvariable = self.pump_state)
        self.devco_label_pumpRunning.grid(column = 0, row = 0, columnspan = 4, sticky=S+W+N+E)

        # PUMP SLIDER
        self.devco_slider_pumpValue = Scale(self.devco_hydro_frame, orient= HORIZONTAL, command= self.update_pump, to = 255)
        self.devco_slider_pumpValue.grid(column = 0, row = 1, columnspan = 4, sticky=S+W+N+E)

        # TOGGLE PUMP STATE
        self.devco_button_pumpEnable = Button(self.devco_hydro_frame, command = self.set_pumpEnable, text = "Enable pump")
        self.devco_button_pumpEnable.grid(column = 0, row = 2, columnspan = 2, sticky=S+W+N+E)

        self.devco_button_pumpDisable = Button(self.devco_hydro_frame, command = self.set_pumpDisable, text = "Disable pump")
        self.devco_button_pumpDisable.grid(column = 2, row = 2, columnspan = 2, sticky=S+W+N+E)

        self.devco_relay1 = Checkbutton(self.devco_hydro_frame, text= NAME_RELAY_1, variable = self.enable_relay1, onvalue= 1, offvalue=0, command = self.toggle_relay1)
        self.devco_relay1.grid(column = 0, row = 3, columnspan = 4, sticky=S+W+N)

        self.devco_relay2 = Checkbutton(self.devco_hydro_frame, text= NAME_RELAY_2, variable = self.enable_relay2, onvalue= 1, offvalue=0, command = self.toggle_relay2)
        self.devco_relay2.grid(column = 0, row = 4, columnspan = 4, sticky=S+W+N)

# P L O T   F R A M E  
        self.plotFrame = Frame(self.contentFrame, bd=1, relief = SUNKEN)
        self.plotFrame.pack(fill = Y, side = LEFT)
        
    # ADD CANVAS TO FRAME
        self.plot_canvas = FigureCanvasTkAgg(f, self.plotFrame)
        self.plot_canvas.show()
        self.plot_canvas.get_tk_widget().pack()

        self.pack()

# prepare animation buffer
BUFF_LEN = 4096
BUFF_FILL = 0
valM = np.zeros( shape=(2,BUFF_LEN) )
valH = np.zeros( shape=(2,BUFF_LEN) )

##   A N I M A T I O N
def animate(i):
    global BUFF_FILL, valM, valH

    # ADD SAMPLE TIME
    for n in range(BUFF_LEN):
        valM[0,n]= -1*(n*(ANI_CYCLETIME/60000.0)) # cycle time defined in ms -> /60000 = min
        valH[0,n]= -1*(n*(ANI_CYCLETIME/60000.0)) # cycle time defined in ms -> /60000 = min

    # SHIFT BUFFERS
    for n in reversed(range( 1, BUFF_LEN )):
        valM[1,n]= valM[1,n-1]
        valH[1,n]= valH[1,n-1]

    # ADD VALUES TO BUFFERS
    tmpVal = app.arduino.readCommand("GET_MOISTURE")
    # tmpVal = str( valM[1,0] + 1 )
    app.moisture_var.set(tmpVal)

    try:
        float(tmpVal)
    except ValueError:
        valM[1,0] = float(0)
    else:
        valM[1,0] = float(tmpVal)

    tmpVal = app.arduino.readCommand("GET_TEMP")
    #tmpVal = str( (valH[1,0]+1) % 2 )
    app.temperature_var.set(tmpVal)

    try:
        float(tmpVal)
    except ValueError:
        valH[1,0] = float(0)
    else:
        valH[1,0] = float(tmpVal)

    # reverse value array for neatness
    valMneat = np.flip(valM, 1)
    valHneat = np.flip(valH, 1)

    # do plot stuff
    if BUFF_FILL < BUFF_LEN:
        BUFF_FILL = BUFF_FILL + 1

#    UPDATE MOUSTURE PLOT
    moistPlot.clear()

    moistPlot.set_ylim([ min(valMneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                        max(valMneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
    # moistPlot.set_ylim([0,100])

    moistPlot.set_ylabel("% of FSV [%]")
    moistPlot.set_xlabel("time [min]")

    moistPlot.grid(True)    
    moistPlot.plot( valMneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valMneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )
    
    
#   UPDATE TEMOERATURE PLOT
    heatPlot.clear()

    heatPlot.set_ylim([ min(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                        max(valHneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
    # heatPlot.set_ylim([15,60])

    heatPlot.set_ylabel("temp [*C]")
    heatPlot.set_xlabel("time [min]")

    heatPlot.grid(True)
    heatPlot.plot( valHneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valHneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )
    # print(BUFF_FILL)

#  A D D   P L O T
f = pp.Figure(figsize=(6,8),dpi = 100)
f.set_tight_layout(True)

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
moistPlot.plot(0, 0)
heatPlot.plot(0, 0)

#run app
root = Tk() #init Tk
root.title ("G R O W  .  M A S T E R")
app = App(master=root)  # assign tk to master frame

def program():
    eptime = time.time()
    struct_time = time.localtime(eptime)

    if struct_time.tm_hour < 10:
        struct_time_str = "0" + str(struct_time.tm_hour) + " : "
    else:
        struct_time_str = str(struct_time.tm_hour) + " : "

    if struct_time.tm_min < 10:
        struct_time_str = struct_time_str + "0" + str(struct_time.tm_min) + " : "
    else:
        struct_time_str = struct_time_str+ str(struct_time.tm_min) + " : "

    if struct_time.tm_sec < 10:
        struct_time_str = struct_time_str + "0" + str(struct_time.tm_sec)
    else:
        struct_time_str = struct_time_str+ str(struct_time.tm_sec)

    app.str_time.set(struct_time_str)

    if app.enable_daylight.get() == 1:

        if struct_time.tm_hour == int(float(app.daylight_tv_start_hour.get())):
            if struct_time.tm_min >= int(float(app.daylight_tv_start_min.get())):
                app.daybool = True
                app.nightbool = False
            else:
                app.daybool = False
        if struct_time.tm_hour == int(float(app.daylight_tv_end_hour.get())):
            if struct_time.tm_min >= int(float(app.daylight_tv_end_min.get())):
                app.nightbool = True
                app.daybool = False
            else:
                app.nightbool = False
        else:
            if struct_time.tm_hour > int(float(app.daylight_tv_start_hour.get())) and struct_time.tm_hour < int(float(app.daylight_tv_end_hour.get())):
                app.daybool = True
                app.nightbool = False
            else:
                app.daybool = False
                app.nightbool = True

        if app.daybool:
        # TIME IS ABOVE DAY START TIME
            if (app.daylight_output < int(app.daylight_brightness.get())):
            # OUTPUT IS NOT YET DONE RISING
                app.daylight_output = float(app.daylight_output) + float(app.daylight_stepsize)
                app.arduino.writeCommand("SET_LAMP", ["W", str(int(app.daylight_output))])
                app.arduino.writeCommand("ENABLE_LAMP", ["1"])

                app.daylight_status.set("DAYTIME - SUNRISE")
                app.lamp_state.set("AUTOMATIC CTRL - RAMPING UP")
                app.devco_slider_lamp.set(int(app.daylight_output))
            else:
                # OUTPUT IS DONE RISING
                app.arduino.writeCommand("SET_LAMP", ["W", str(int(float(app.daylight_brightness.get())))])
                app.arduino.writeCommand("ENABLE_LAMP", ["1"])

                app.daylight_status.set("DAYTIME")
                app.lamp_state.set("AUTOMATIC CTRL - FULL OUTPUT")
                app.devco_slider_lamp.set(int(float(app.daylight_brightness.get())))

        elif app.nightbool:
            if (app.daylight_output > 0):
            # OUTPUT IS NOT YET DONE FALLING
                app.daylight_output = app.daylight_output - app.daylight_stepsize
                app.arduino.writeCommand("SET_LAMP", ["W", str(int(float(app.daylight_output)))])
                app.arduino.writeCommand("ENABLE_LAMP", ["1"])

                app.daylight_status.set("DAYTIME - SUNSET")
                app.lamp_state.set("AUTOMATIC CTRL - RAMPING DOWN")
                app.devco_slider_lamp.set(int(app.daylight_output))
            else:
           # OUTPUT IS NOT YET DONE FALLING
                app.arduino.writeCommand("SET_LAMP", ["W", str(0)])
                app.arduino.writeCommand("ENABLE_LAMP", ["0"])

                app.daylight_status.set("NIGHTTIME")
                app.lamp_state.set("AUTOMATIC CTRL - DISABLED OUTPUT")
                app.devco_slider_lamp.set(0)

    else:
        app.daylight_status.set("DAYLIGHT DISABLED")
        app.lamp_state.set("LAMP DISABLED")


    if app.arduino.getStatus():
        app.serial_connection_string.set("Connected")
    else:
        app.serial_connection_string.set("Disconnected")


    

    root.after(int(PROGRAM_CYLCETIME), program)
root.after(int(PROGRAM_CYLCETIME), program)

ani = animation.FuncAnimation(f, animate, interval = int(ANI_CYCLETIME))
app.mainloop()
app.arduino.closeConnection()
sys.exit()
