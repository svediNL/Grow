from math import *
import matplotlib 
from matplotlib import pyplot as pp
import matplotlib.animation as animation
from matplotlib import gridspec
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
from configuration import *

import time

FIRST_SCAN = True

# prepare animation buffer
BUFF_FILL = 0
valM = np.zeros( shape=(2,BUFF_LEN) )
valH = np.zeros( shape=(2,BUFF_LEN) )
valH1 = np.zeros( shape=(2,BUFF_LEN) )
valP = np.zeros( shape=(2,BUFF_LEN) )
valL = np.zeros( shape=(2,BUFF_LEN) )
time_list = []
label_list = []
tick_list = []
clear_list = []

# FILL SAMPLE TIME
for n in range(BUFF_LEN):
    valM[0,n]  = -n # -1*(n*(ANI_CYCLETIME/60000.0)) # cycle time defined in ms -> /60000 = min
    valH[0,n]  = -n #-1*(n*(ANI_CYCLETIME/60000.0)) # cycle time defined in ms -> /60000 = min
    valH1[0,n] = -n #-1*(n*(ANI_CYCLETIME/60000.0)) # cycle time defined in ms -> /60000 = min
    valP[0,n]  = -n #-1*(n*(ANI_CYCLETIME/60000.0)) # cycle time defined in ms -> /60000 = min
    valL[0,n]  = -n #-1*(n*(ANI_CYCLETIME/60000.0)) # cycle time defined in ms -> /60000 = min

valMneat  = np.flip(valM, 1)
valHneat  = np.flip(valH, 1)
valH1neat = np.flip(valH1, 1)
valPneat  = np.flip(valP, 1)
valLneat  = np.flip(valL, 1)

# DEFINE APP CLASS AS BASE FRAME
class App( Frame ):

#   INIT
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # PUMP VARIABLES
        self.pump_enable = []
        self.pump_enable_prev = []
        self.pump_state = []
        self.pump_pwm = []
        self.overrule_pump_interlock = []
        for n in range(NR_PUMP):
            self.pump_enable.append(False)
            self.pump_enable_prev.append(False)
            self.pump_pwm.append(0)
            self.pump_state.append(StringVar())
            self.pump_state[n].set("pump stopped...")
            self.overrule_pump_interlock.append(IntVar())

        # RELAY
        self.enable_relay=[]
        self.enable_relay_prev=[]
        for n in range(NR_RELAY):
            self.enable_relay.append(IntVar())
            self.enable_relay_prev.append(self.enable_relay[n].get())
        
        self.flow_state = IntVar()
        self.flow_state.set(NR_FLOW)

        self.flow_control_relays = []
        for n in range( len(VALVES_FLOW) ):
            for m in range( len(VALVES_FLOW[n]) ):
                if len(self.flow_control_relays) > 0:
                    append_valves_list = True
                    for k in range(len(self.flow_control_relays)):
                        if self.flow_control_relays[k] == VALVES_FLOW[n][m]:
                            append_valves_list = False
                    if append_valves_list:
                        self.flow_control_relays.append(VALVES_FLOW[n][m])
                else:
                    print "except"
                    self.flow_control_relays.append(VALVES_FLOW[n][m])
                print self.flow_control_relays
        self.flow_control_relays.sort()
        print self.flow_control_relays


        # LAMP
        self.lamp_enable =[]
        self.lamp_enable_prev = []
        self.lamp_output=[]         #  [LAMP_INDEX] [LAMP_CHANNEL]
        self.lamp_output_prev =[] 
        self.lamp_state = []
        for n in range(NR_LAMP):
            print n
            self.lamp_enable.append(False)
            self.lamp_enable_prev.append(False)
            self.lamp_state.append(StringVar())
            self.lamp_state[n].set("LAMP DISABLED")

            tmp0 = []
            tmp1 =[]
            for m in range(len(CHANNELS_LAMP[n])):
                tmp0.append(IntVar())
                tmp1.append(0)
            self.lamp_output.append(tmp0)
            self.lamp_output_prev.append(tmp1)

        
        print self.lamp_output

        self.moisture_var = []
        for n in range(NR_MOISTURE):
            self.moisture_var.append(StringVar())

        self.temperature_var = []
        for n in range(NR_THERMO):
            self.temperature_var.append(StringVar())

        # DAYLIGHT SEQUENCE VARIABLES
        self.enable_daylight = IntVar()
        self.daylight_status = StringVar()
        self.daylight_brightness = StringVar()
        self.daylight_tv_start_hour = StringVar()
        self.daylight_tv_start_min = StringVar()
        self.daylight_tv_end_hour = StringVar()
        self.daylight_tv_end_min = StringVar()
        self.daylight_tv_ramp_hour = StringVar()
        self.daylight_tv_ramp_min = StringVar()

        # SET DAYLIGHT VARIABLES
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

        # SERIAL VARIABLES
        self.serial_var_string = StringVar()
        self.serial_connection_string = StringVar()
        self.serial_var_port = StringVar()
        self.serial_var_port.set("/dev/ttyACM0")
        self.arduino = SlaveComm("/dev/ttyACM0", 115200)

        # CREATE WIDGETS
        self.create_widgets()

        # GET/SET STATUS ON ARDUINO
        if self.arduino.getStatus():
            self.serial_connection_string.set("Connected")

            # WRITE DEFAULT VALUES
            for i in range(NR_RELAY):
                self.enable_relay[i].set(0)
                self.arduino.writeCommand( "SET_RELAY", [str(i), str(self.enable_relay[i].get())] )
 
            for i in range(NR_PUMP):
                self.devco_slider_pumpValue.set(0)
                self.pump_enable[i] = False
                self.arduino.writeCommand( "SET_PUMP", [str(i) ,str(self.devco_slider_pumpValue.get()), str(int(self.pump_enable[i]))] )

            for i in range(len(self.lamp_output)):
                for j in range(len(self.lamp_output[i])):
                    self.lamp_output[i][j].set(0)
                    self.arduino.writeCommand("SET_LAMP", [str(i),str(CHANNELS_LAMP[i][j]), str(int(float( self.lamp_output[i][j].get() )))])
        else:
            self.serial_connection_string.set("Disconnected")

#   SERIAL FUNCTIONS
    def open_serial_connection(self):
        self.arduino.setPort(self.serial_var_port.get())
        self.arduino.openConnection()

        if self.arduino.getStatus():
            self.serial_connection_string.set("Connected")

            # WRITE DEFAULT VALUES
            for i in range(NR_RELAY):
                self.arduino.writeCommand( "SET_RELAY", [str(i), str(self.enable_relay[i].get())] )
 
            for i in range(NR_PUMP):
                self.arduino.writeCommand( "SET_PUMP", [ str(i),str(self.pump_pwm[0]), str(int(self.pump_enable[0]))] )

            for i in range(len(self.lamp_output)):
                for j in range(len(self.lamp_output[i])):
                    self.arduino.writeCommand("SET_LAMP", [str(i),str(CHANNELS_LAMP[i][j]), str(int(float( self.lamp_output[i][j].get() )))])

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

#   LIGHTING FUNCTIONS
    def disable_lamp(self):
        self.lamp_state[0].set("LAMP DISABLED")
        self.arduino.writeCommand("ENABLE_LAMP", ["0","0"])

        self.enable_relay[6].set(0)     # FANS ON LAMP
        self.toggle_relay()

    def enable_lamp(self):
        self.lamp_state[0].set("LAMP ENABLED")
        self.arduino.writeCommand("ENABLE_LAMP", ["0","1"])

        self.enable_relay[0].set(1)     # ENABLE 12V (FOR FAN & PWM LEVEL BOOSTER)
        self.enable_relay[6].set(1)     # FANS ON LAMP
        self.toggle_relay()

    def update_lamp(self, value):
        # CYLCLE TRHOUGH OUTPUT CHANNELS
        for n in range(len(self.lamp_output)):
            for m in range(len(self.lamp_output[n])):
                if self.lamp_output[n][m].get() != self.lamp_output_prev[n][m]:
                    # OUTPUT CHANNEL HAS CHANGED
                    self.lamp_output_prev[n][m] = self.lamp_output[n][m].get()
                    self.arduino.writeCommand("SET_LAMP", [str(n),str(CHANNELS_LAMP[n][m]), str(int(float(value)))])

    def update_daylight_params(self):
        try:
            if float(self.daylight_tv_ramp_min.get())>0 or float(self.daylight_tv_ramp_hour.get())>0:
                self.daylight_stepsize = float(self.daylight_brightness.get()) / ( ( float(self.daylight_tv_ramp_hour.get())*3600 + float(self.daylight_tv_ramp_min.get())*60 ) / float(PROGRAM_CYLCETIME/1000) )
                print self.daylight_stepsize
        except ValueError:
            print "Value Error"

        if self.enable_daylight.get() ==0:
            self.enable_relay[0].set(0)     # ENABLE 12V (FOR FAN & PWM LEVEL BOOSTER)
            self.enable_relay[6].set(0)     # FANS ON LAMP
            self.toggle_relay()

        elif self.enable_daylight.get() ==1:
            self.enable_relay[0].set(1)     # ENABLE 12V (FOR FAN & PWM LEVEL BOOSTER)
            self.enable_relay[6].set(1)     # FANS ON LAMP
            self.toggle_relay()

        return True 

#   HYDROLIC FUNCTIONS
    def update_pump(self, value):
        self.pump_pwm[0] = int(float(value))
        self.arduino.writeCommand("SET_PUMP", ["0",str(self.pump_pwm[0]), str(int(self.pump_enable[0]))] )
        if self.pump_enable[0]:
            self.pump_state[0].set("PUMP & VALVES ENABLED")
            self.toggle_pump_interlock()
        else:
            self.pump_state[0].set("PUMP STOPPED")

    def set_pumpEnable(self):
        for n in range(NR_PUMP):
            self.pump_enable[n] = True
            self.arduino.writeCommand("ENABLE_PUMP", ["0",str(int(self.pump_enable[0]))])
            self.pump_state[0].set("PUMP & VALVES ENABLED")
            self.set_flow_circuit()

    def set_pumpDisable(self):
        self.pump_enable[0] = False
        self.arduino.writeCommand("ENABLE_PUMP", ["0",str(0)])
        self.pump_state[0].set("PUMP STOPPED")
        self.reset_flow_circuit()


    def toggle_pump_interlock(self):
        if FORCE_INTERLOCK[self.flow_state.get()] == True:
            app.overrule_pump_interlock[0].set(0)

        if self.overrule_pump_interlock[0].get() == 0:
            self.arduino.writeCommand("IGNORE_PUMP_INTERLOCK", ["0",str(0)])
        else:
            self.arduino.writeCommand("IGNORE_PUMP_INTERLOCK", ["0",str(1)])

    def set_flow_circuit(self):
    # SET VALVES BASED ON SELECTED FLOW CIRCUIT
        self.reset_flow_circuit()

        # OPEN VALVES BASED ON SELECTED FLOW CIRCUIT
        if self.flow_state.get() == NR_FLOW:
        # DEFAULT = DO NOTHING
            print "DISABLED"
        else:
        # OPEN VALVES
            for m in range(len( VALVES_FLOW[self.flow_state.get()] )):
                print VALVES_FLOW[self.flow_state.get()][m]
                tmp = VALVES_FLOW[self.flow_state.get()][m]
                self.enable_relay[tmp].set(1)

        # WRITE/SET ACTUAL OUTPUT
        self.toggle_relay()
        self.toggle_pump_interlock()

    def reset_flow_circuit(self):
    # DEFAULT ALL VALVES TO CLOSED
        for n in range(NR_RELAY):
        # ITERATE VALVE INDEX
            for m in range(len(self.flow_control_relays)):
            # ITERATE FLOW CONTROL VALVE INDEX
                if n == self.flow_control_relays[m]:
                # SET VALVE RELAY 0
                    self.enable_relay[n].set(0)

        # WRITE/SET ACTUAL OUTPUT
        self.toggle_relay()

    def toggle_relay(self):
        for n in range(NR_RELAY):
            if self.enable_relay_prev[n] != self.enable_relay[n].get():
                self.enable_relay_prev[n] = self.enable_relay[n].get()
                self.arduino.writeCommand("SET_RELAY", [str(n), str(self.enable_relay[n].get())])

#   BUILD GUI
    def create_widgets(self):
    # M A I N   F R A M E

        # CREATE MAIN FRAME
        self.mainframe = Frame(self, bd=4, relief = SUNKEN , bg = "white")
        #self.mainframe.pack(fill = BOTH, expand = True)
        self.mainframe.grid(column = 0, row=0, sticky=E+W)
        self.mainframe.grid_columnconfigure(0, weight =1)
        self.mainframe.grid_columnconfigure(1, weight =1)
        
    # H E A D E R   F R A M E
        # CREATE HEADER FRAME
        self.headerFrame=Frame(self.mainframe, bd=2, relief = SUNKEN , bg = "white")
        #self.headerFrame.pack(fill = BOTH, side = TOP, expand = True)
        self.headerFrame.grid(column = 0, columnspan = 2, row=0, sticky=N+S+E+W)
        self.headerFrame.grid_columnconfigure(0, weight =1)
        self.headerFrame.grid_columnconfigure(1, weight =1)

        # HEADER TEXT
        self.label_header = Label(self.headerFrame, text= " +- ~ - ~ - ~ - ~ - ~ -+  G R O W   M A S T E R     v1.6  +- ~ - ~ - ~ - ~ - ~ -+ " , bg = "white")
        #self.label_header.pack(side = LEFT)
        self.label_header.grid(column = 0, row=0, sticky=N+S+W)

        # CURRENT TIME LABEL
        self.label_time = Label(self.headerFrame, textvariable = self.str_time , bg = "white")
        #self.label_time.pack(side = RIGHT)
        self.label_time.grid(column = 1, row=0, sticky=N+S+E)


    # C O N T E N T   F R A M E
        # CREATE CONTENT FRAME (PLOT AREA)
        self.contentFrame=Frame(self.mainframe, bd=2, relief = SUNKEN, bg = "white")
        #self.contentFrame.pack(side = BOTTOM, expand = True)
        self.contentFrame.grid(column = 0, row=1, columnspan = 2, sticky=N+S+E+W)
        self.contentFrame.grid_columnconfigure(0, weight =2)
        self.contentFrame.grid_columnconfigure(1, weight =1)

    # P L O T   F R A M E  
        self.plotFrame = Frame(self.contentFrame, bd=2, relief = SUNKEN, bg = "white")
        #self.plotFrame.pack(fill = Y, side = LEFT, expand = True)
        self.plotFrame.grid(column = 0, row=0, sticky=N+S+E+W)
        self.plotFrame.grid_columnconfigure(0, weight =1)

        # ADD NOTEBOOK TO SERIAL FRAME
        self.plot_notebook = Notebook(self.plotFrame)
        self.plot_notebook.pack(fill = BOTH, side = LEFT, expand = True)
        #self.plot_notebook.grid(column = 0, row=0, sticky=N+S+E+W)  

        # ADD CONNECTION FRAME TO NOTEBOOK
        self.plot_overviewFrame = Frame(self.plot_notebook)
        self.plot_notebook.add(self.plot_overviewFrame, text = 'overview')

        # ADD CONNECTION FRAME TO NOTEBOOK
        self.plot_hydroFrame = Frame(self.plot_notebook)
        self.plot_notebook.add(self.plot_hydroFrame, text = 'hydro')

        # ADD CONNECTION FRAME TO NOTEBOOK
        self.plot_lightFrame = Frame(self.plot_notebook)
        self.plot_notebook.add(self.plot_lightFrame, text = 'light')

        # ADD CANVAS TO FRAME
        self.plot_canvas = FigureCanvasTkAgg(f, self.plot_overviewFrame)
        self.plot_canvas.show()
        self.plot_canvas.get_tk_widget().pack(side= RIGHT, fill = BOTH, expand = True)

        # ADD CANVAS TO FRAME
        self.plot_canvas1 = FigureCanvasTkAgg(f1, self.plot_hydroFrame)
        self.plot_canvas1.show()
        self.plot_canvas1.get_tk_widget().pack(side= RIGHT, fill = BOTH, expand = True)

        # ADD CANVAS TO FRAME
        self.plot_canvas2 = FigureCanvasTkAgg(f2, self.plot_lightFrame)
        self.plot_canvas2.show()
        self.plot_canvas2.get_tk_widget().pack(side= RIGHT, fill = BOTH, expand = True)


    # D I R E C T   C O N T R O L   F R A M E
        # CREATE DIRECT CONTROL FRAME
        self.dicoFrame = Frame(self.contentFrame, bd=2, relief = SUNKEN, bg = "white") # width = 600,
        #self.dicoFrame.pack(fill = BOTH, side = RIGHT, expand = True)

        self.dicoFrame.grid(column = 1, row=0, sticky=N+S+E+W)
        self.dicoFrame.grid_columnconfigure(0,weight=1)
        self.dicoFrame.grid_rowconfigure(0,weight=1)
        self.dicoFrame.grid_rowconfigure(1,weight=1)
        self.dicoFrame.grid_rowconfigure(2,weight=2)

    #   S E R I A L  F R A M E
        # ADD SERIAL FRAME TO DICO FRAME
        self.serial_frame = Frame(self.dicoFrame, bd=1, bg = "white", relief = SUNKEN)
        #self.serial_frame.pack(side = TOP, fill = Y, expand = True)
        self.serial_frame.grid(column = 0, row=0, sticky=N+S+E+W)
        self.serial_frame.grid_columnconfigure(0,weight=1)
        self.serial_frame.grid_rowconfigure(0,weight=1)
        self.serial_frame.grid_rowconfigure(1,weight=2)

        # SERIAL HEADER TEXT
        self.serial_header_frame = Frame(self.serial_frame, bg = "gray93")
        self.serial_header_frame.grid(column = 0, row=0, sticky=N+S+E+W)
        self.serial_header_frame.grid_columnconfigure(0,weight=1)

        self.serial_header_label = Label(self.serial_header_frame, text = "~  S E R I A L ", bg = "gray93")
        self.serial_header_label.grid(column = 0, row=0, sticky=N+S+W)

        # ADD NOTEBOOK TO SERIAL FRAME
        self.serial_notebook_frame = Frame(self.serial_frame, bg = "white")
        self.serial_notebook_frame.grid(column = 0, row=1, sticky=N+S+E+W)
        self.serial_notebook_frame.grid_columnconfigure(0,weight=1)
        self.serial_notebook_frame.grid_rowconfigure(0,weight=1)

        self.serial_notebook = Notebook(self.serial_notebook_frame) #, width = 300)
        self.serial_notebook.grid(column = 0, row=0, sticky=N+S+E+W)

        # ADD CONNECTION FRAME TO NOTEBOOK
        self.serial_connectionFrame = Frame(self.serial_notebook, bg = "white")
        self.serial_notebook.add(self.serial_connectionFrame, text = 'connect')
        
        # ADD PROMPT FOR PORT TO CONNECTION FRAME
        self.serial_entry_port = Entry(self.serial_connectionFrame, textvariable= self.serial_var_port)
        self.serial_entry_port.pack(side= TOP, fill = X)

        # ADD LABEL FOR STATUS TO CONNECTION FRAME
        self.serial_label_status = Label(self.serial_connectionFrame, textvariable = self.serial_connection_string)
        self.serial_label_status.pack(side= TOP, fill = X, expand = True)

        # ADD OPEN CONNECTION BUTTON TO CONNECTION FRAME
        self.serial_button_open= Button(self.serial_connectionFrame, text = "open", command= self.open_serial_connection)
        self.serial_button_open.pack(side= RIGHT, fill = X, expand = True)

        self.serial_button_close = Button(self.serial_connectionFrame,text = "close", command= self.close_serial_connection)
        self.serial_button_close.pack(side = RIGHT, fill = X, expand = True)

        # SERIAL NOTEBOOK _ DIRECT INTERFACE
        self.serial_interfaceFrame = Frame(self.serial_notebook, bg = "white")    
        self.serial_notebook.add(self.serial_interfaceFrame, text = 'comm')

        self.serial_entry_command = Entry(self.serial_interfaceFrame, textvariable= self.serial_var_string)
        self.serial_entry_command.pack(side= TOP, fill = X)

        self.serial_button_read= Button(self.serial_interfaceFrame, text = "read", command= self.read_serial_string)
        self.serial_button_read.pack(side = LEFT, fill = BOTH, expand =True)

        self.serial_button_write= Button(self.serial_interfaceFrame, text = "write", command= self.write_serial_string)
        self.serial_button_write.pack(side = LEFT, fill = BOTH, expand =True)


    #   L I V E   S T A T U S   F R A M E
        # ADD LIVE STATUS FRAME TO DICO FRAME
        self.live_frame = Frame(self.dicoFrame, bd=1, relief= SUNKEN, bg = "white")
        self.live_frame.grid_columnconfigure(0, weight =1)
        # self.live_frame.grid_columnconfigure(1, weight =1)
        self.live_frame.grid_rowconfigure(0, weight =1)
        self.live_frame.grid_rowconfigure(1, weight =2)

        #self.live_frame.pack(fill = BOTH, side = TOP, expand = True)
        self.live_frame.grid(column = 0, row=1, sticky=N+S+E+W)

        self.live_header_frame = Frame(self.live_frame, bg = "white")
        self.live_header_frame.grid(column = 0, row=0, sticky=N+S+E+W)
        self.live_header_frame.grid_rowconfigure(0, weight =1)

        self.live_content_frame = Frame(self.live_frame, bg = "white")
        self.live_content_frame.grid(column = 0, row=1, sticky=N+S+E+W)
        self.live_content_frame.grid_columnconfigure(0, weight =0)
        self.live_content_frame.grid_columnconfigure(1, weight =3)
        self.live_content_frame.grid_columnconfigure(2, weight =0)
        self.live_content_frame.grid_columnconfigure(3, weight =0)

        self.live_label = Label(self.live_header_frame, text = "~ L I V E   M O N I T O R", bg = "white")
        self.live_label.grid(column = 0, row = 0, sticky = N+S+W)

        self.live_content_frame.grid_rowconfigure(0, weight =2)
        self.live_top_padding = Label(self.live_content_frame, text = "", bg = "white")
        self.live_top_padding.grid(column = 0, row = 0, columnspan = 2, sticky = N+S+W)

        self.color_index = 0
        self.color_toggle = ["white","gray75"]
        self.live_heat_label = []
        self.live_heat_pad =[]
        self.live_heat_value = []
        self.live_heat_unit = []
        for n in range(NR_THERMO):
            tmp = NAMES_THERMO[n] + " :   "
            row_nr = (n+1)
            self.live_content_frame.grid_rowconfigure(row_nr, weight =3)

            self.live_heat_label.append(Label(self.live_content_frame, text = tmp, bg = self.color_toggle[self.color_index % 2] ))
            self.live_heat_label[n].grid(column = 0, row= row_nr, sticky=N+S+W+E)
            self.live_heat_pad.append(Label(self.live_content_frame, text = "", bg = self.color_toggle[self.color_index % 2] ))
            self.live_heat_pad[n].grid(column = 1, row= row_nr, sticky=N+S+W+E)
            self.live_heat_value.append(Label(self.live_content_frame, textvariab = self.temperature_var[n], bg = self.color_toggle[self.color_index % 2] ))
            self.live_heat_value[n].grid(column = 2, row= row_nr, sticky=N+S+E+W)
            self.live_heat_unit.append(Label(self.live_content_frame, text = UNIT_THERMO, bg = self.color_toggle[self.color_index % 2] ))
            self.live_heat_unit[n].grid(column = 3, row= row_nr, sticky=N+S+E+W)
            self.color_index = self.color_index + 1
            

        self.live_moist_label = []
        self.live_moist_value = []
        self.live_moist_pad =[]
        self.live_moist_unit = []
        for n in range(NR_MOISTURE):
            tmp = NAMES_MOISTURE[n] + "  :   "
            row_nr = (NR_THERMO+n+1)
            self.live_content_frame.grid_rowconfigure(row_nr, weight =3)

            self.live_moist_label.append(Label(self.live_content_frame, text = tmp, bg = self.color_toggle[self.color_index % 2] ))
            self.live_moist_label[n].grid(column = 0, row= row_nr, sticky=N+S+W+E)
            self.live_moist_pad.append(Label(self.live_content_frame, text = "", bg = self.color_toggle[self.color_index % 2] ))
            self.live_moist_pad[n].grid(column = 1, row= row_nr, sticky=N+S+W+E)
            self.live_moist_value.append(Label(self.live_content_frame, textvariab = self.moisture_var[n], bg = self.color_toggle[self.color_index % 2] ))
            self.live_moist_value[n].grid(column = 2, row= row_nr, sticky=N+S+E+W)
            self.live_moist_unit.append(Label(self.live_content_frame, text = UNIT_MOISTURE, bg = self.color_toggle[self.color_index % 2] ))
            self.live_moist_unit[n].grid(column = 3, row= row_nr, sticky=N+S+E+W)
            self.color_index = self.color_index + 1
            
        row_nr = (NR_THERMO+NR_MOISTURE+1)
        self.live_content_frame.grid_rowconfigure(0, weight =2)
        self.live_bottom_padding = Label(self.live_content_frame, text = "", bg = "white")
        self.live_bottom_padding.grid(column = 0, row = row_nr, columnspan = 2, sticky = N+S+W)

    #   D E V I C E  C O N T R O L  F R A M E
        # ADD DEVICE CONTROL TO DICOFRAME
        self.devco_frame = Frame(self.dicoFrame , bd=1, relief = SUNKEN, bg = "gray93")
        #self.devco_frame.pack(fill = Y, side = TOP, expand = True)
        self.devco_frame.grid(column = 0, row=2, sticky=N+S+E+W)
        self.devco_frame.grid_columnconfigure(0,weight=1)

        # DEVICE CONTROL HEADER TEXT
        self.devco_label = Label(self.devco_frame, text= "~  D E V I C E  C O N T R O L ", bg = "gray93")
        self.devco_label.grid(column = 0, row=0, sticky=N+S+W)

        # DEVICE CONTROL NOTEBOOL
        self.devco_notebook = Notebook(self.devco_frame) #, width = 300
        self.devco_notebook.grid(column = 0, row=1, sticky=N+S+E+W)

    #   DEVCO NOTBOOK _ LAMP CONTROL
        self.devco_lamp_frame = Frame(self.devco_notebook, bg = "white")
        self.devco_notebook.add(self.devco_lamp_frame, text = 'LIGHT', sticky=N+S+E+W)
        self.devco_lamp_notebook = Notebook(self.devco_lamp_frame)
        self.devco_lamp_notebook.pack(side=TOP , fill = BOTH)

        self.devco_label_lampName = []
        self.devco_label_lampState = []
        self.devco_label_slider= []
        self.devco_slider_lamp=[]
        self.devco_button_lampOff=[]
        self.devco_button_lampOn=[]
        self.devco_lamp_direct_frame=[]
        for n in range(NR_LAMP):
            self.devco_lamp_direct_frame.append(Frame(self.devco_lamp_frame, bd=2, relief = SUNKEN, bg = "white"))
            self.devco_lamp_notebook.add(self.devco_lamp_direct_frame[n], text = NAMES_LAMP[n], sticky =N+S+E+W)
            self.devco_lamp_direct_frame[n].grid_columnconfigure(0, weight =1)
            self.devco_lamp_direct_frame[n].grid_columnconfigure(1, weight =1)
            self.devco_lamp_direct_frame[n].grid_columnconfigure(2, weight =1)
            self.devco_lamp_direct_frame[n].grid_columnconfigure(3, weight =1)
            # LAMP STATE
            self.devco_label_lampName.append(Label(self.devco_lamp_direct_frame[n], text = NAMES_LAMP[n]))
            self.devco_label_lampName[n].grid(column = 0, row = (3*n)+0)

            self.devco_label_lampState.append(Label(self.devco_lamp_direct_frame[n], textvariable = self.lamp_state[n]))
            self.devco_label_lampState[n].grid(column = 1, columnspan = 3, row = (3*n)+0)

            tmp0 = []
            tmp1 = []
            for m in range(len(CHANNELS_LAMP[n])):
                # SLIDER LABELS
                tmp0.append(Label(self.devco_lamp_direct_frame[n], text=(CHANNELS_LAMP[n][m] + "-channel")))
                tmp1.append(Scale(self.devco_lamp_direct_frame[n], orient= HORIZONTAL, variable = self.lamp_output[n][m], command= self.update_lamp, to = 255))

            self.devco_label_slider.append(tmp0)
            self.devco_slider_lamp.append(tmp1)   

            for m in range(len(CHANNELS_LAMP[n])):
                # SLIDERS
                self.devco_label_slider[n][m].grid(column = 0, row = (3*n)+m+1, sticky=S+W)
                self.devco_slider_lamp[n][m].grid(column = 1, row = (3*n)+m+1, columnspan = 3, sticky=S+W+N+E)

            # ON BUTTON
            self.devco_button_lampOff.append(Button(self.devco_lamp_direct_frame[n], text= "OFF", command = self.disable_lamp))
            self.devco_button_lampOff[n].grid(column = 0, columnspan = 2, row = (3*n)+len(CHANNELS_LAMP[n])+1, sticky=N+S+E+W)

            # OFF BUTTON
            self.devco_button_lampOn.append(Button(self.devco_lamp_direct_frame[n], text= "ON", command = self.enable_lamp))
            self.devco_button_lampOn[n].grid(column = 2, columnspan = 2, row = (3*n)+len(CHANNELS_LAMP[n])+1, sticky=N+S+E+W)

        # AUTOMATIC LIGHT MODE
        self.devco_lamp_daylight_frame = Frame(self.devco_lamp_frame, bd=2, relief = SUNKEN, bg = "white")
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

    #   DEVCO NOTBOOK _ HYDROLICS
        self.devco_hydro_frame = Frame(self.devco_notebook)
        self.devco_hydro_frame.grid_columnconfigure(0, weight =1)
        self.devco_hydro_frame.grid_columnconfigure(1, weight =1)
        self.devco_hydro_frame.grid_columnconfigure(2, weight =1)
        self.devco_hydro_frame.grid_columnconfigure(3, weight =1)
        self.devco_notebook.add(self.devco_hydro_frame, text = 'HYDROLICS', sticky=N+S+E+W)

        # PUMP RUNNING FB
        self.devco_label_pumpRunning = Label(self.devco_hydro_frame, textvariable = self.pump_state[0])
        self.devco_label_pumpRunning.grid(column = 0, row = 0, columnspan = 4, sticky=S+W+N+E)

        # PUMP SLIDER
        self.devco_slider_pumpValue = Scale(self.devco_hydro_frame, orient= HORIZONTAL, command= self.update_pump, to = 255)
        self.devco_slider_pumpValue.grid(column = 0, row = 1, columnspan = 4, sticky=S+W+N+E)

        # TOGGLE PUMP STATE
        self.devco_button_pumpEnable = Button(self.devco_hydro_frame, command = self.set_pumpEnable, text = "Enable pump")
        self.devco_button_pumpEnable.grid(column = 0, row = 2, columnspan = 2, sticky=S+W+N+E)

        self.devco_button_pumpDisable = Button(self.devco_hydro_frame, command = self.set_pumpDisable, text = "Disable pump")
        self.devco_button_pumpDisable.grid(column = 2, row = 2, columnspan = 2, sticky=S+W+N+E)

        self.devco_check_overrule_pump = Checkbutton(self.devco_hydro_frame, variable = self.overrule_pump_interlock[0], onvalue= 1, offvalue=0, command = self.toggle_pump_interlock, text = "Overrule Pump Interlock")
        self.devco_check_overrule_pump.grid(column = 0, row = 3, columnspan = 4, sticky=S+W+N+E)

        self.devco_flow=[]
        for n in range(NR_FLOW):
            self.devco_flow.append(Radiobutton(self.devco_hydro_frame, text= NAMES_FLOW[n], value = n, variable = self.flow_state, command = self.set_flow_circuit))
            self.devco_flow[n].grid(column = 0, row = (4+n), columnspan = 4, sticky=S+W+N)
        self.devco_flow.append(Radiobutton(self.devco_hydro_frame, text= "DISABLED", value = NR_FLOW, variable = self.flow_state, command = self.set_flow_circuit))
        self.devco_flow[NR_FLOW].grid(column = 0, row = (4+NR_FLOW), columnspan = 4, sticky=S+W+N)

    #   DEVCO NOTBOOK _ RELAY CONTROL
        self.devco_relay_frame = Frame(self.devco_notebook)
        self.devco_relay_frame.grid_columnconfigure(0, weight =1)
        self.devco_relay_frame.grid_columnconfigure(1, weight =1)
        self.devco_relay_frame.grid_columnconfigure(2, weight =1)
        self.devco_relay_frame.grid_columnconfigure(3, weight =1)
        self.devco_notebook.add(self.devco_relay_frame, text = 'RELAYS', sticky=N+S+E+W)

        self.devco_relay = []
        for n in range(NR_RELAY):
            self.devco_relay.append(Checkbutton(self.devco_relay_frame, text= NAMES_RELAY[n], variable = self.enable_relay[n], onvalue= 1, offvalue=0, command = self.toggle_relay))
            self.devco_relay[n].grid(column = 0, row = n, columnspan = 4, sticky=S+W+N)

        # SET BACKGROUND CLOUR
        if DEBUG_MODE:
            self.configure(bg='red')
            self.mainframe.configure(bg='green')
            self.headerFrame.configure(bg='blue')
            self.contentFrame.configure(bg='yellow')
            self.plotFrame.configure(bg='orange')
            self.dicoFrame.configure(bg='magenta')
        else:
            self.configure(bg='white')
            self.mainframe.configure(bg='white')
            self.headerFrame.configure(bg='white')
            self.contentFrame.configure(bg='white')
            self.plotFrame.configure(bg='white')
            self.dicoFrame.configure(bg='white')

    #   PACK SELF
        self.grid_columnconfigure(0, weight =1)
        self.grid_rowconfigure(0, weight =1)
        self.pack(fill = BOTH, expand = True)

    def daylight_sequence(self):
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

        self.str_time.set(struct_time_str)

        if self.enable_daylight.get() == 1:
            if struct_time.tm_hour == int(float(self.daylight_tv_start_hour.get())):
            # CURRENT = START HOUR
                if struct_time.tm_min >= int(float(self.daylight_tv_start_min.get())):
                # CURRENT = START MINUTE
                    self.daybool = True
                    self.nightbool = False

            elif struct_time.tm_hour > int(float(self.daylight_tv_start_hour.get())) and struct_time.tm_hour < int(float(self.daylight_tv_end_hour.get())):
            #  START HOUR < CURRENT < END HOUR
                    self.daybool = True
                    self.nightbool = False
            elif struct_time.tm_hour == int(float(self.daylight_tv_end_hour.get())):
            # CURRENT = END HOUR
                if struct_time.tm_min >= int(float(self.daylight_tv_start_min.get())):
                # CURRENT = END MINUTE
                    self.daybool = False
                    self.nightbool = True
            else:
            # NOT BETWEEN START OR END -> SO NIGHT
                self.daybool = False
                self.nightbool = True

            if self.daybool:
            # TIME IS ABOVE DAY START TIME
                if (self.daylight_output < int(self.daylight_brightness.get())):
                # OUTPUT IS NOT YET DONE RISING
                    self.daylight_output = float(self.daylight_output) + float(self.daylight_stepsize)
                    self.arduino.writeCommand("SET_LAMP", ["W", str(int(self.daylight_output))])
                    self.arduino.writeCommand("ENABLE_LAMP", ["0","1"])

                    self.daylight_status.set("DAYTIME - SUNRISE")
                    self.lamp_state[0].set("AUTOMATIC CTRL - RAMPING UP")
                    self.devco_slider_lamp[0][0].set(int(self.daylight_output))
                else:
                    # OUTPUT IS DONE RISING
                    self.arduino.writeCommand("SET_LAMP", ["W", str(int(float(self.daylight_brightness.get())))])
                    self.arduino.writeCommand("ENABLE_LAMP", ["0","1"])

                    self.daylight_status.set("DAYTIME")
                    self.lamp_state[0].set("AUTOMATIC CTRL - FULL OUTPUT")
                    self.devco_slider_lamp[0][0].set(int(float(self.daylight_brightness.get())))

            elif self.nightbool:
                if (self.daylight_output > 0):
                # OUTPUT IS NOT YET DONE FALLING
                    self.daylight_output = self.daylight_output - self.daylight_stepsize
                    self.arduino.writeCommand("SET_LAMP", ["W", str(int(float(self.daylight_output)))])
                    self.arduino.writeCommand("ENABLE_LAMP", ["0","1"])

                    self.daylight_status.set("DAYTIME - SUNSET")
                    self.lamp_state[0].set("AUTOMATIC CTRL - RAMPING DOWN")
                    self.devco_slider_lamp[0][0].set(int(self.daylight_output))
                else:
               # OUTPUT IS NOT YET DONE FALLING
                    self.arduino.writeCommand("SET_LAMP", ["W", str(0)])
                    self.arduino.writeCommand("ENABLE_LAMP", ["0","0"])

                    self.daylight_status.set("NIGHTTIME")
                    self.lamp_state[0].set("AUTOMATIC CTRL - DISABLED OUTPUT")
                    self.devco_slider_lamp[0][0].set(0)

        else:
            self.daylight_status.set("DAYLIGHT DISABLED")

##   A N I M A T I O N
def animate(i):
# PLOT VALUES
    global BUFF_FILL, FIRST_SCAN
    global valM, valH, valH1, valP, valL
    global valMneat,valHneat, valH1neat, valPneat, valLneat
    global time_list, label_list, tick_list, clear_list

    if not FIRST_SCAN and BUFF_FILL>0:
    # UPDATE PLOTS
        if DEBUG_MODE:
            print " "
            print "= = = = = = = = = = = ="
            print "   A N I M A T E   0   "
            print app.plot_notebook.index(app.plot_notebook.select())
            start_plot = time.time()
            start = time.time()

    #   F - UPDATE TEMOERATURE PLOT
        heatPlot.clear()
        hy_min = min(min(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), min(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) - 1
        hy_max = max(max(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), max(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) + 1
        heatPlot.set_ylim([ hy_min, hy_max ])
        heatPlot.set_ylabel("TC Temp [*C]")
            # SET X TICK TIME LABEL
        if BUFF_FILL > 1:
            heatPlot.set_xticks(tick_list)
            heatPlot.set_xticklabels(clear_list)
        heatPlot.grid(True)
        heatPlot.plot( valHneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valHneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='g' )
        heatPlot.plot( valH1neat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valH1neat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='b' )

    #   F - UPDATE LAMP
        lampPlot.clear()
        lampPlot.set_ylim([ min(valLneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                            max(valLneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
        lampPlot.set_ylabel("LIGHT")

        # SET X TICK TIME LABEL
        if BUFF_FILL > 1:
            lampPlot.set_xticks(tick_list)
            lampPlot.set_xticklabels(clear_list)
        lampPlot.grid(True)
        lampPlot.plot( valLneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valLneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

    #   F - UPDATE MOUSTURE PLOT
        moistPlot.clear()
        moistPlot.set_ylim([ min(valMneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                            max(valMneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
        moistPlot.set_ylabel("Moisture [%]")

        # SET X TICK TIME LABEL
        if BUFF_FILL > 1:
            moistPlot.set_xticks(tick_list)
            moistPlot.set_xticklabels(clear_list)
        moistPlot.grid(True)   
        moistPlot.plot( valMneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valMneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

    #   F - UPDATE PUMP
        pumpPlot.clear()
        pumpPlot.set_ylim([ min(valPneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                            max(valPneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
        pumpPlot.set_ylabel("PUMP")
        pumpPlot.set_xlabel("time [min]")

        # SET X TICK TIME LABEL
        if BUFF_FILL > 1:
            pumpPlot.set_xticks(tick_list)
            pumpPlot.set_xticklabels(label_list, rotation =45)

        pumpPlot.grid(True)
        pumpPlot.plot( valPneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valPneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

        # PRINT PLOTTING TIME
        if DEBUG_MODE:
            end = time.time()
            print "plot time: " + str(end-start)
            print "BUFF_FILL: " + str(BUFF_FILL)
                
        if DEBUG_MODE:
            end_plot = time.time()
            print " "
            print "ANIMATE time: " + str(end_plot-start_plot)
            print "= = = = = = = = = = = ="
            print " "

    if FIRST_SCAN:
        FIRST_SCAN = False

def animate1(i):
# PLOT VALUES
    global BUFF_FILL, FIRST_SCAN
    global valM, valP
    global valMneat, valPneat
    global time_list, label_list, tick_list, clear_list


    if not FIRST_SCAN and BUFF_FILL>0:
    # UPDATE PLOTS
        if DEBUG_MODE:
            print " "
            print "= = = = = = = = = = = ="
            print "   A N I M A T E   1   "
            print app.plot_notebook.index(app.plot_notebook.select())
            start_plot = time.time()
            start = time.time()


    #   F1 - UPDATE MOUSTURE PLOT
        moistPlot1.clear()
        moistPlot1.set_ylim([ min(valMneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                            max(valMneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
        moistPlot1.set_ylabel("Moisture [%]")

        # SET X TICK TIME LABEL
        if BUFF_FILL > 1:
            moistPlot1.set_xticks(tick_list)
            moistPlot1.set_xticklabels(clear_list)
        moistPlot1.grid(True)   
        moistPlot1.plot( valMneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valMneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

    #   F1 - UPDATE PUMP
        pumpPlot1.clear()
        pumpPlot1.set_ylim([ min(valPneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                            max(valPneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
        pumpPlot1.set_ylabel("PUMP")
        pumpPlot1.set_xlabel("time [min]")

        # SET X TICK TIME LABEL
        if BUFF_FILL > 1:
            pumpPlot1.set_xticks(tick_list)
            pumpPlot1.set_xticklabels(label_list, rotation =45)

        pumpPlot1.grid(True)
        pumpPlot1.plot( valPneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valPneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

        # PRINT PLOTTING TIME
        if DEBUG_MODE:
            end = time.time()
            print "plot time: " + str(end-start)
            print "BUFF_FILL: " + str(BUFF_FILL)
            
        if DEBUG_MODE:
            end_plot = time.time()
            print " "
            print "ANIMATE time: " + str(end_plot-start_plot)
            print "= = = = = = = = = = = ="
            print " "

    if FIRST_SCAN:
        FIRST_SCAN = False

def animate2(i):
# PLOT VALUES
    global BUFF_FILL, FIRST_SCAN
    global valH, valH1, valL
    global valHneat, valH1neat, valLneat
    global time_list, label_list, tick_list, clear_list

    if not FIRST_SCAN and BUFF_FILL>0:
    # UPDATE PLOTS
        if DEBUG_MODE:
            print " "
            print "= = = = = = = = = = = ="
            print "   A N I M A T E   2   "
            print app.plot_notebook.index(app.plot_notebook.select())
            start_plot = time.time()
            start = time.time()

    #   F2 - UPDATE TEMOERATURE PLOT
        heatPlot2.clear()
        hy2_min = min(min(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), min(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) - 1
        hy2_max = max(max(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), max(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) + 1
        heatPlot2.set_ylim([ hy2_min, hy2_max ])
        heatPlot2.set_ylabel("TC Temp [*C]")
            # SET X TICK TIME LABEL
        if BUFF_FILL > 1:
            heatPlot2.set_xticks(tick_list)
            heatPlot2.set_xticklabels(clear_list)
        heatPlot2.grid(True)
        heatPlot2.plot( valHneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valHneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='g' )
        heatPlot2.plot( valH1neat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valH1neat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='b' )

    #   F2 - UPDATE LAMP
        lampPlot2.clear()
        lampPlot2.set_ylim([ min(valLneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                            max(valLneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
        lampPlot2.set_ylabel("LIGHT")

        # SET X TICK TIME LABEL
        if BUFF_FILL > 1:
            lampPlot2.set_xticks(tick_list)
            lampPlot2.set_xticklabels(label_list, rotation =45)
        lampPlot2.grid(True)
        lampPlot2.plot( valLneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valLneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

        # PRINT PLOTTING TIME
        if DEBUG_MODE:
            end = time.time()
            print "plot time: " + str(end-start)
            print "BUFF_FILL: " + str(BUFF_FILL)
                
        if DEBUG_MODE:
            end_plot = time.time()
            print " "
            print "ANIMATE time: " + str(end_plot-start_plot)
            print "= = = = = = = = = = = ="
            print " "

    if FIRST_SCAN:
        FIRST_SCAN = False

def update_plot(index):
    global BUFF_FILL, FIRST_SCAN
    global valM, valH, valH1, valP, valL
    global valMneat,valHneat, valH1neat, valPneat, valLneat
    global time_list, label_list, tick_list, clear_list

    if index == 0:
        if not FIRST_SCAN and BUFF_FILL>0:
            print "index 0"
        #   F - UPDATE TEMOERATURE PLOT
            heatPlot.clear()
            hy_min = min(min(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), min(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) - 1
            hy_max = max(max(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), max(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) + 1
            heatPlot.set_ylim([ hy_min, hy_max ])
            heatPlot.set_ylabel("TC Temp [*C]")
                # SET X TICK TIME LABEL
            if BUFF_FILL > 1:
                heatPlot.set_xticks(tick_list)
                heatPlot.set_xticklabels(clear_list)
            heatPlot.grid(True)
            heatPlot.plot( valHneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valHneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='g' )
            heatPlot.plot( valH1neat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valH1neat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='b' )

        #   F - UPDATE LAMP
            lampPlot.clear()
            lampPlot.set_ylim([ min(valLneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                                max(valLneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
            lampPlot.set_ylabel("LIGHT")

            # SET X TICK TIME LABEL
            if BUFF_FILL > 1:
                lampPlot.set_xticks(tick_list)
                lampPlot.set_xticklabels(clear_list)
            lampPlot.grid(True)
            lampPlot.plot( valLneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valLneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

        #   F - UPDATE MOUSTURE PLOT
            moistPlot.clear()
            moistPlot.set_ylim([ min(valMneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                                max(valMneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
            moistPlot.set_ylabel("Moisture [%]")

            # SET X TICK TIME LABEL
            if BUFF_FILL > 1:
                moistPlot.set_xticks(tick_list)
                moistPlot.set_xticklabels(clear_list)
            moistPlot.grid(True)   
            moistPlot.plot( valMneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valMneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

        #   F - UPDATE PUMP
            pumpPlot.clear()
            pumpPlot.set_ylim([ min(valPneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                                max(valPneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
            pumpPlot.set_ylabel("PUMP")
            pumpPlot.set_xlabel("time [min]")

            # SET X TICK TIME LABEL
            if BUFF_FILL > 1:
                pumpPlot.set_xticks(tick_list)
                pumpPlot.set_xticklabels(label_list, rotation =45)

            pumpPlot.grid(True)
            pumpPlot.plot( valPneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valPneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

    elif index == 1:
        if not FIRST_SCAN and BUFF_FILL>0:
            print "index 1"
        #   F1 - UPDATE MOUSTURE PLOT
            moistPlot1.clear()
            moistPlot1.set_ylim([ min(valMneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                                max(valMneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
            moistPlot1.set_ylabel("Moisture [%]")

            # SET X TICK TIME LABEL
            if BUFF_FILL > 1:
                moistPlot1.set_xticks(tick_list)
                moistPlot1.set_xticklabels(clear_list)
            moistPlot1.grid(True)   
            moistPlot1.plot( valMneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valMneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

        #   F1 - UPDATE PUMP
            pumpPlot1.clear()
            pumpPlot1.set_ylim([ min(valPneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                                max(valPneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
            pumpPlot1.set_ylabel("PUMP")
            pumpPlot1.set_xlabel("time [min]")

            # SET X TICK TIME LABEL
            if BUFF_FILL > 1:
                pumpPlot1.set_xticks(tick_list)
                pumpPlot1.set_xticklabels(label_list, rotation =45)

            pumpPlot1.grid(True)
            pumpPlot1.plot( valPneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valPneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

    elif index == 2:
        if not FIRST_SCAN and BUFF_FILL>0:
            print "index 2"
        #   F2 - UPDATE TEMOERATURE PLOT
            heatPlot2.clear()
            hy2_min = min(min(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), min(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) - 1
            hy2_max = max(max(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), max(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) + 1
            heatPlot2.set_ylim([ hy2_min, hy2_max ])
            heatPlot2.set_ylabel("TC Temp [*C]")
                # SET X TICK TIME LABEL
            if BUFF_FILL > 1:
                heatPlot2.set_xticks(tick_list)
                heatPlot2.set_xticklabels(clear_list)
            heatPlot2.grid(True)
            heatPlot2.plot( valHneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valHneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='g' )
            heatPlot2.plot( valH1neat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valH1neat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='b' )

        #   F2 - UPDATE LAMP
            lampPlot2.clear()
            lampPlot2.set_ylim([ min(valLneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1, 
                                max(valLneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1 ])
            lampPlot2.set_ylabel("LIGHT")

            # SET X TICK TIME LABEL
            if BUFF_FILL > 1:
                lampPlot2.set_xticks(tick_list)
                lampPlot2.set_xticklabels(label_list, rotation =45)
            lampPlot2.grid(True)
            lampPlot2.plot( valLneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valLneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )


## START PROGRAM / GUI
#  DEFINE MATPLOT FUIGURE
f = pp.Figure(figsize=(10,10),dpi = 75)
gs = gridspec.GridSpec(4,1, height_ratios=[3,1,3,1])
f.set_tight_layout(True)

f1 = pp.Figure(figsize=(10,10),dpi = 75)
gs1 = gridspec.GridSpec(2,1, height_ratios=[3,2])
f1.set_tight_layout(True)

f2 = pp.Figure(figsize=(10,10),dpi = 75)
gs2 = gridspec.GridSpec(2,1, height_ratios=[3,2])
f2.set_tight_layout(True)

# ADD SUBPLOTS
heatPlot = f.add_subplot(gs[0])
lampPlot = f.add_subplot(gs[1])
moistPlot = f.add_subplot(gs[2])
pumpPlot = f.add_subplot(gs[3])

moistPlot1 = f1.add_subplot(gs1[0])
pumpPlot1 = f1.add_subplot(gs1[1])

heatPlot2 = f2.add_subplot(gs2[0])
lampPlot2 = f2.add_subplot(gs2[1])

# SET Y LIMITS
heatPlot.set_ylim([10,40])
lampPlot.set_ylim([0,255])
moistPlot.set_ylim([0,100])
pumpPlot.set_ylim([0,100])

moistPlot1.set_ylim([0,100])
pumpPlot1.set_ylim([0,100])

heatPlot2.set_ylim([10,40])
lampPlot2.set_ylim([0,255])

# SET Y LABEL
heatPlot.set_ylabel("TC temp [*C]")
lampPlot.set_ylabel("LIGHT")
moistPlot.set_ylabel("Moisture [%]")
pumpPlot.set_ylabel("PUMP")

moistPlot1.set_ylabel("Moisture [%]")
pumpPlot1.set_ylabel("PUMP")

heatPlot2.set_ylabel("TC temp [*C]")
lampPlot2.set_ylabel("LIGHT")

# SETT GRID
heatPlot.grid(True)
lampPlot.grid(True)
moistPlot.grid(True)
pumpPlot.grid(True)

moistPlot1.grid(True)
pumpPlot1.grid(True)

heatPlot2.grid(True)
lampPlot2.grid(True)


pumpPlot.set_xlabel("time [min]")

heatPlot.plot([0,1], [10,40])
lampPlot.plot([0,1], [0,255])
moistPlot.plot([0,1], [0,100])
pumpPlot.plot([0,1], [0,100])

moistPlot1.plot([0,1], [0,100])
pumpPlot1.plot([0,1], [0,100])

heatPlot2.plot([0,1], [10,40])
lampPlot2.plot([0,1], [0,255])


# DEFINE TK STUFF
root = Tk() #init Tk
root.title ("G R O W  .  M A S T E R")
app = App(master=root)  # assign tk to master frame

cycle_counter = 0
plot_index_prev = 0
plot_index = 0

# PROGRAM TO CALL EVERY .. 
def program():
    global BUFF_FILL, FIRST_SCAN
    global valM, valH, valH1, valP, valL
    global valMneat,valHneat, valH1neat, valPneat, valLneat
    global time_list, label_list, tick_list, clear_list
    global cycle_counter, plot_index, plot_index_prev


    if DEBUG_MODE:
        print " "
        print "= = = = = = = = = = = ="
        print "   P R O G R A M   "
        start_prog = time.time()

    # CALL DAYLIGHT SCHEDULER
    app.daylight_sequence()

#   UPDATE ARDUINO STATUS
    if app.arduino.getStatus():
        app.serial_connection_string.set("Connected")

    else:
        app.serial_connection_string.set("Disconnected")

#   GET NEW SAMPLES
    tick_list = []
    label_list = []
    clear_list = []

    # RESET COUNTER IF IT IS TIME TO SAMPLE
    if cycle_counter >= SAMPLE_RATE:
        cycle_counter = 0

    # GET SAMPLE IF ARDUINO IS CONNECTED
    if not FIRST_SCAN and (app.arduino.assumed_connection_status or DEBUG_MODE) and cycle_counter == 0:

        if DEBUG_MODE:
            start = time.time()

#   SHIFT BUFFERS IN REVERSED ORDER
        for n in reversed(range( 1, BUFF_LEN )):
            valM[1,n]= valM[1,n-1]
            valH[1,n]= valH[1,n-1]
            valH1[1,n]= valH1[1,n-1]
            valP[1,n]= valP[1,n-1]
            valL[1,n]= valL[1,n-1]  

        if  DEBUG_MODE:
            end = time.time()
            print "- Shift buffers: " + str(end-start)
            start = time.time()

#   ADD VALUES TO BUFFERS
    #   HEAT
        if DEBUG_MODE:
            tmpVal = str( (valH[1,0]+1) % 2 )
        else:
            tmpVal = app.arduino.readCommand("GET_TEMP",["0"])

        app.temperature_var[0].set(tmpVal)
        try:
            float(tmpVal)
        except ValueError:
            valH[1,0] = float(0)
        else:
            valH[1,0] = float(tmpVal)  

    #   HEAT 1
        if DEBUG_MODE:
            tmpVal = str( ((valH1[1,0]+1)*7) % 3 ) 
        else:
            tmpVal = app.arduino.readCommand("GET_TEMP",["1"])
        app.temperature_var[1].set(tmpVal)
        try:
            float(tmpVal)
        except ValueError:
            valH1[1,0] = float(0)
        else:
            valH1[1,0] = float(tmpVal)   

    #   MOISTURE
        if DEBUG_MODE:
            tmpVal = str( valM[1,0] + 1 )
        else:
            tmpVal = app.arduino.readCommand("GET_MOISTURE",["0"])
        app.moisture_var[0].set(tmpVal)

        try:
            float(tmpVal)
        except ValueError:
            valM[1,0] = float(0)
        else:
            valM[1,0] = float(tmpVal)

    #   PUMP
        if DEBUG_MODE:
            tmpVal = str( (valP[1,0]+1) % 2 )
        else:
            tmpVal = app.arduino.readCommand("GET_PUMP",["0"])
        try:
            float(tmpVal)
        except ValueError:
            valP[1,0] = float(0)
        else:
            valP[1,0] = float(tmpVal)
        
    #   LIGHT
        if DEBUG_MODE:
            tmpVal = str( (valL[1,0]+1) % 2 )
        else:
            tmpVal = app.arduino.readCommand("GET_LAMP",["0"])
        try:
            float(tmpVal)
        except ValueError:
            valL[1,0] = float(0)
        else:
            valL[1,0] = float(tmpVal)

        if DEBUG_MODE:
            end = time.time()
            print "- Get values: " + str(end-start)

        if BUFF_FILL < BUFF_LEN:
            BUFF_FILL = BUFF_FILL + 1

#   FLIP BUFFERS
        # reverse value array for neatness
        valMneat = np.flip(valM, 1)
        valHneat = np.flip(valH, 1)
        valH1neat = np.flip(valH1, 1)
        valPneat = np.flip(valP, 1)
        valLneat = np.flip(valL, 1)
        
#   MAKE LICK LIST
        time_list.insert(0, app.str_time.get())
        if BUFF_FILL>1:
            if BUFF_FILL>6:
                label_list = []
                tick_list = []
                stepsize = BUFF_FILL/6.0

                for n in range(6):
                    label_list.append(time_list[int(n*stepsize)])
                    tick_list.append(valP[0,int(n*stepsize)])
                    clear_list.append("")
                label_list.append(time_list[BUFF_FILL-1])
                tick_list.append(valP[0,BUFF_FILL-1])
                clear_list.append("")

            else:
                label_list = []
                tick_list = []
                clear_list = []
                for n in range(BUFF_FILL-1):
                    label_list.append(time_list[int(n)])
                    tick_list.append(valP[0,n])
                    clear_list.append("")
                label_list.append(time_list[BUFF_FILL-1])
                tick_list.append(valP[0,BUFF_FILL-1])
                clear_list.append("")

#   UPDATE PLOT ON TAB CHANGE
    plot_index = app.plot_notebook.index(app.plot_notebook.select())
    if plot_index != plot_index_prev:
        print " - TAB CHANGED - "
        update_plot(plot_index)
    plot_index_prev = plot_index

    if DEBUG_MODE:
        end_prog = time.time()
        print " "
        print "PROGRAM() time: " + str(end_prog-start_prog)
        print "= = = = = = = = = = = ="
        print " "

#   UPDATE CYCLE COUNTER AND SCHEDULE NEW PROGRAM CYCLE
    cycle_counter = cycle_counter + 1
    FIRST_SCAN = False
    root.after(int(PROGRAM_CYLCETIME), program)
root.after(int(PROGRAM_CYLCETIME), program)

# START GUI
ani = animation.FuncAnimation(f, animate, interval = int(ANI_CYCLETIME))
ani1 = animation.FuncAnimation(f1, animate1, interval = int(ANI_CYCLETIME))
ani2 = animation.FuncAnimation(f2, animate2, interval = int(ANI_CYCLETIME))
app.mainloop()
app.arduino.closeConnection()
sys.exit()
