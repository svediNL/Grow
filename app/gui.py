print(".  .  .  .  .  .  .  .  .  .  .  .  .  .")
print("+~~+~~+~~+    Grow    v2.0    +~~+~~+~~+")
print("^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^")
print("")

try:
    from Tkinter import *
    from ttk import *
    from Tkinter import messagebox
except:
    print("> using execeptional tkinter")
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
else:
    print("> using regular Tkinter")

from math import *

print("> import matplotlib stuff")
import matplotlib 
matplotlib.use("TkAgg")
from matplotlib import pyplot as pp
import matplotlib.animation as animation
from matplotlib import gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

print("> import numpy")
import numpy as np

from comms import SlaveComm
from configuration import *

print("> import pandas stuff")
import pandas as pd
import os.path

print("> import time, maaan")
import time

import warnings

FIRST_SCAN = True
PLOT_WINDOW = 0

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

def get_time_list():
    global time_list
    return time_list

def get_label_list():
    global label_list
    return label_list

def get_tick_list():
    global tick_list
    return tick_list

def get_clear_list():
    global clear_list
    return clear_list

def set_time_list(val):
    global time_list
    time_list = val

def set_label_list(val):
    global label_list
    label_list = val

def set_tick_list(val):
    global tick_list
    tick_list = val

def set_clear_list(val):
    global clear_list
    clear_list = val

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

        print("> app _init_")
        self.style = ttk.Style()
        # https://www.tcl.tk/man/tcl/TkCmd/ttk_notebook.htm#M10
        self.style.theme_create( "myStyle", 
                                 parent="default", 
                                 settings=  {   "TNotebook": { "configure": 
                                                                 { "tabmargins": [7, 13, 4, 0],
                                                                   "background": BG_MAIN,
                                                                   "foreground": BG_MAIN,
                                                                   "lightcolor": BG_MAIN,
                                                                   "darkcolor": BG_MAIN }    # direction: <, ^, >, v
                                                             },
                                                "TNotebook.Tab": { "configure": 
                                                                        { "padding": [5, 1], 
                                                                          "background": BG_TAB,
                                                                          "foreground": FG_TEXT },
                                                                    "map":
                                                                        { "background": [("selected", BG_TAB_ACTIVE)], 
                                                                          "expand": [("selected", [3, 2, 3, 1])] } 
                                                                 }
                                            }
                                )
        self.style.theme_use("myStyle")

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
            self.pump_state.append(StringVar(master))
            self.pump_state[n].set("pump stopped...")
            self.overrule_pump_interlock.append(IntVar(master))

        # RELAY
        self.enable_relay=[]
        self.enable_relay_prev=[]
        for n in range(NR_RELAY):
            self.enable_relay.append(IntVar(master))
            self.enable_relay_prev.append(self.enable_relay[n].get())
        
        self.flow_state = IntVar(master)
        self.flow_state.set(NR_FLOW)
        self.flow_state_prev = NR_FLOW
        self.plot_select = IntVar(master) # add master because it is accessed externally
        self.plot_select.set(0)
        self.plot_select_prev = 0

        # FIND & ADD ALL RELAYS RELATED TO VALVE CIRCUIT
        self.flow_control_relays = []
        for n in range( len(VALVES_FLOW) ):
        # CYCLE FLOW CIRCUITS
            for m in range( len(VALVES_FLOW[n]) ):
            # CYCLE VALVES IN FLOW CICRUIT
                if len(self.flow_control_relays) == 0:
                # FIST INDEX
                    self.flow_control_relays.append(VALVES_FLOW[n][m])

                else:
                # CHECK IF CURRENT VALUE IS ALREADY IN LIST
                    append_valves_list = True # default
                    for k in range(len(self.flow_control_relays)):
                        if self.flow_control_relays[k] == VALVES_FLOW[n][m]:
                            append_valves_list = False

                    # APPEND VALVE IF NOT YET PRESENT
                    if append_valves_list:
                        self.flow_control_relays.append(VALVES_FLOW[n][m])

        # SORT LIST
        self.flow_control_relays.sort()
        print("> Relays used in flow:" , str(self.flow_control_relays))


        # LAMP
        self.lamp_enable =[]
        self.lamp_enable_prev = []
        self.lamp_output=[]         #  [LAMP_INDEX] [LAMP_CHANNEL]
        self.lamp_output_prev =[] 
        self.lamp_state = []
        for n in range(NR_LAMP):
            self.lamp_enable.append(False)
            self.lamp_enable_prev.append(False)
            self.lamp_state.append(StringVar(master))
            self.lamp_state[n].set("LAMP DISABLED")

            tmp0 = []
            tmp1 =[]
            for m in range(len(CHANNELS_LAMP[n])):
                tmp0.append(IntVar(master))
                tmp1.append(0)
            self.lamp_output.append(tmp0)
            self.lamp_output_prev.append(tmp1)

        self.moisture_var = []
        for n in range(NR_MOISTURE):
            self.moisture_var.append(StringVar(master))

        self.temperature_var = []
        for n in range(NR_THERMO):
            self.temperature_var.append(StringVar(master))

        # DAYLIGHT SEQUENCE VARIABLES
        self.enable_daylight = IntVar(master)
        self.daylight_status = StringVar(master)
        self.daylight_brightness = StringVar(master)
        self.daylight_tv_start_hour = StringVar(master)
        self.daylight_tv_start_min = StringVar(master)
        self.daylight_tv_end_hour = StringVar(master)
        self.daylight_tv_end_min = StringVar(master)
        self.daylight_tv_ramp_hour = StringVar(master)
        self.daylight_tv_ramp_min = StringVar(master)

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

        self.str_time = StringVar(master)
        self.str_time.set(".....")

        # SERIAL VARIABLES
        self.serial_var_string = StringVar(master)
        self.serial_connection_string = StringVar(master)
        self.serial_entry_string = StringVar(master)
        self.serial_var_port = StringVar(master)
        self.serial_var_port.set(SERIAL_PORT)

        self.arduino = SlaveComm(SERIAL_PORT, BAUD_RATE)
        self.serial_port_list = self.arduino.get_ports()
        self.serial_port_hist = [SERIAL_PORT]
        self.serial_combo_list = []
        self.serial_combo_sel = 0

        self.schedule_devices     = ["NONE", "PUMP", "LAMP"]    # DEVICES THAT CAN BE USED FOR SCHEDULING
        self.schedule_sel         = [0,0,0,0,0,0,0,0,0,0]                       # LIST OF CURRENT SELECTED DEVICE FOR COMBOBOX
        self.schedule_sel_prev    = [0,0,0,0,0,0,0,0,0,0]                       # PREVIOUSLY SELECTED DEVICE (FOR DETECTING CHANGE)
        self.schedule_sel_id      = [0,0,0,0,0,0,0,0,0,0]                       # LIST OF CURRENT SELECTED DEVICE FOR COMBOBOX
        self.schedule_var_start   = []
        self.schedule_var_ontime  = []
        self.schedule_var_value   = []
        for n in range(len(self.schedule_sel)):
            self.schedule_var_start.append(StringVar(master))
            self.schedule_var_start[n].set("00:00:00")

            self.schedule_var_ontime.append(StringVar(master))
            self.schedule_var_ontime[n].set("0")

            self.schedule_var_value.append(StringVar(master))
            self.schedule_var_value[n].set("0")

        print("> app _init_   Frame._init_(self)")
        Frame.__init__(self, master)

        # CREATE WIDGETS
        print("> app _init_   createWidgets()")
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

        print(">app _init_   finished")

#   SERIAL FUNCTIONS
    def open_serial_connection(self):
        self.arduino.setPort(self.serial_var_port.get())
        self.serial_port_hist.append(self.serial_var_port.get())
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
        tmp_string = self.arduino.writeString(self.serial_var_string.get())
        self.serial_entry_string.set( tmp_string )
        self.serial_var_string.set("")
        
    def read_serial_string(self):
        tmp_string = "< " #+self.arduino.readString(self.serial_var_string.get())
        self.serial_entry_string.set(tmp_string)
        self.serial_var_string.set("")
        
    def postcom_port_list(self):
        # BUILD LIST OF PORT HISTORY & AVAILABLE PORTS
        self.serial_combo_list = [""] # EMPTY ITEM FOR NO SELECTION
        for n in range(len(self.serial_port_hist)):
            self.serial_combo_list.append(self.serial_port_hist[n]) # APPEND HISTORY
        for n in range(len(self.serial_port_list)):
            self.serial_combo_list.append(self.serial_port_list[n]) # APPEND AVAILABLE PORTS
        self.serial_combo_port['values'] = self.serial_combo_list   # SET LIST

    def update_serial(self):
        if self.serial_combo_sel != self.serial_combo_port.current() and self.serial_combo_port.get() != "":
            self.serial_var_port.set(self.serial_combo_port.get())
            self.serial_combo_sel = self.serial_combo_port.current()

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
                print(self.lamp_output[n][m].get())
                if self.lamp_output[n][m].get() != self.lamp_output_prev[n][m]:
                    # OUTPUT CHANNEL HAS CHANGED
                    self.lamp_output_prev[n][m] = self.lamp_output[n][m].get()
                    self.arduino.writeCommand("SET_LAMP", [str(n),str(CHANNELS_LAMP[n][m]), str(int(float(value))), str(int(self.lamp_enable[n]))])

    def update_daylight_params(self):
        try:
            if float(self.daylight_tv_ramp_min.get())>0 or float(self.daylight_tv_ramp_hour.get())>0:
                self.daylight_stepsize = float(self.daylight_brightness.get()) / ( ( float(self.daylight_tv_ramp_hour.get())*3600 + float(self.daylight_tv_ramp_min.get())*60 ) / float(PROGRAM_CYLCETIME/1000) )
                print(self.daylight_stepsize)
        except ValueError:
            print("Value Error")

        if self.enable_daylight.get() ==0:
            self.enable_relay[0].set(0)     # ENABLE 12V (FOR FAN & PWM LEVEL BOOSTER)
            self.enable_relay[6].set(0)     # FANS ON LAMP
            self.toggle_relay()

        elif self.enable_daylight.get() ==1:
            self.enable_relay[0].set(1)     # ENABLE 12V (FOR FAN & PWM LEVEL BOOSTER)
            self.enable_relay[6].set(1)     # FANS ON LAMP
            self.toggle_relay()

        return True 

    # DAYLIGHT SEQUENCE
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

        if self.enable_daylight.get() == 1 and self.arduino.getStatus():
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

        # SET & RESET SELECTION COLOUR
        self.devco_flow[ self.flow_state.get() ]["bg"] = BG_SEL
        self.devco_flow[ self.flow_state.get() ]["fg"] = FG_TEXT2
        if self.flow_state_prev % 2 == 0:
            self.devco_flow[ self.flow_state_prev ]["bg"] = BG_TOG_A
            self.devco_flow[ self.flow_state.get() ]["fg"] = FG_TEXT
        else:
            self.devco_flow[ self.flow_state_prev ]["bg"] = BG_TOG_B
            self.devco_flow[ self.flow_state.get() ]["fg"] = FG_TEXT

        # OPEN VALVES BASED ON SELECTED FLOW CIRCUIT
        if self.flow_state.get() == NR_FLOW:
        # DEFAULT = DO NOTHING
            print("DISABLED")
        else:
        # OPEN VALVES
            for m in range(len( VALVES_FLOW[self.flow_state.get()] )):
                print(VALVES_FLOW[self.flow_state.get()][m])
                tmp = VALVES_FLOW[self.flow_state.get()][m]
                self.enable_relay[tmp].set(1)

        # WRITE/SET ACTUAL OUTPUT
        self.toggle_relay()
        self.toggle_pump_interlock()
        self.flow_state_prev = self.flow_state.get()

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

                # SET & RESET SELECTION COLOUR
                if self.enable_relay_prev[n] == 1:
                    self.devco_relay[n]["bg"] = BG_SEL
                    self.devco_relay[n]["fg"] = FG_TEXT2
                else:
                    if n % 2 == 0:
                        self.devco_relay[n]["bg"] = BG_TOG_A
                        self.devco_relay[n]["fg"] = FG_TEXT
                    else:
                        self.devco_relay[n]["bg"] = BG_TOG_B
                        self.devco_relay[n]["fg"] = FG_TEXT

#   PLOT FUNCTIONS
    def get_plot(self):
        return self.plot_select.get()

    def plot_change(self):
        # SET & RESET SELECTION COLOUR
        self.plotbutton[ self.plot_select.get() ]["bg"] = BG_SEL
        self.plotbutton[ self.plot_select.get() ]["fg"] = FG_TEXT2

        self.plotbutton[ self.plot_select_prev ]["bg"] = BG_SUB
        self.plotbutton[ self.plot_select_prev ]["fg"] = FG_TEXT

        self.plot_select_prev = self.plot_select.get()

#   SCHEDULE FUNCTIONS
    def update_schedule_combo(self):
        # CYCLE SCHEDULE DEVICES
        for n in range(len(self.schedule_sel)):
            # UPDATE SELECTIONS
            self.schedule_sel[n] = self.schedule_combo_dev[n].current() 
            #self.schedule_sel_id[n] = self.schedule_combo_id[n].current()

            # BUILD ID LIST
            tmp = []
            if self.schedule_sel[n] <= 0:
                tmp = [-1]
            elif self.schedule_sel[n] == 1:
                for m in range(NR_PUMP):
                    tmp.append(m)
            elif self.schedule_sel[n] == 2:
                for m in range(NR_LAMP):
                    tmp.append(m)
            
            # SET VALUES IN COMBO BOX
            self.schedule_combo_id[n]['values'] = tmp
            self.schedule_sel_prev[n] = self.schedule_sel[n]

    def update_sched_combo_dev(self):
        self.update_schedule_combo()


    def update_sched_combo_id(self):
        self.update_schedule_combo()

        


#   BUILD GUI
    def create_widgets(self):
    # M A I N   F R A M E

        # CREATE MAIN FRAME
        self.mainframe = Frame( self, 
                                bg= BG_MAIN, 
                                bd = 4, 
                                relief = SUNKEN )
        self.mainframe.grid(column = 0, row=0, sticky=N+S+E+W)
        #self.mainframe.pack(fill = BOTH, expand = True)

        self.mainframe.grid_columnconfigure(0, weight =1)
        self.mainframe.grid_columnconfigure(1, weight =1)
        self.mainframe.grid_rowconfigure(0, weight =0)
        self.mainframe.grid_rowconfigure(1, weight =2)

    # H E A D E R   F R A M E
        # CREATE HEADER FRAME
        self.headerFrame=Frame( self.mainframe, 
                                bg      = BG_MAIN, 
                                bd      = 2, 
                                relief  = SUNKEN )
        
        self.headerFrame.grid(column = 0, columnspan = 2, row=0, sticky=N+S+E+W)
        #self.headerFrame.pack(fill = BOTH, side = TOP, expand = True)

        # GRID HEADER FRAME
        self.headerFrame.grid_columnconfigure(0, weight =1)
        self.headerFrame.grid_columnconfigure(1, weight =1)
        self.headerFrame.grid_rowconfigure(0, weight =0)

        # HEADER TEXT
        self.label_header = Label(  self.headerFrame, 
                                    text    = " +- ~ - ~ - ~ - ~ - ~ -+  G R O W   M A S T E R     v2.0  +- ~ - ~ - ~ - ~ - ~ -+ ", 
                                    bg      = BG_MAIN, 
                                    fg      = FG_TEXT, 
                                    bd      = 4)
        self.label_header.grid(column = 0, row=0, sticky=N+S+W)
        #self.label_header.pack(side = LEFT)

        # CURRENT TIME LABEL
        self.label_time = Label(    self.headerFrame, 
                                    textvariable = self.str_time, 
                                    bg           = BG_MAIN, 
                                    fg           = FG_TEXT, 
                                    bd           = 4)
        self.label_time.grid(column = 1, row=0, sticky=N+S+E)
        #self.label_time.pack(side = RIGHT)


    # C O N T E N T   F R A M E
        # CREATE CONTENT FRAME
        self.contentFrame=Frame(    self.mainframe, 
                                    bd      = 2, 
                                    relief  = SUNKEN, 
                                    bg      = BG_MAIN)
        self.contentFrame.grid(column = 0, row=1, columnspan = 2, sticky=N+S+E+W)
        #self.contentFrame.pack(side = BOTTOM, expand = True)

        # GRID CONTENT FRAME
        self.contentFrame.grid_columnconfigure(0, weight =2)
        self.contentFrame.grid_columnconfigure(1, weight =1)
        self.contentFrame.grid_rowconfigure(0, weight =1)

    # P L O T   F R A M E  
        # CREATE PLOT FRAME
        self.plotFrame = Frame( self.contentFrame, 
                                bd=2, 
                                relief = SUNKEN, 
                                bg = BG_MAIN)
        self.plotFrame.grid(column = 0, row=0, sticky=N+S+E+W)
        #self.plotFrame.pack(fill = Y, side = LEFT, expand = True)

        # GRID PLOT FRAME
        self.plotFrame.grid_columnconfigure(0, weight =1)
        self.plotFrame.grid_rowconfigure(0, weight =0)
        self.plotFrame.grid_rowconfigure(1, weight =1)


        # ADD PLOT BUTTON FRAME
        self.plotFrame_button = Frame( self.plotFrame, 
                                bd=0, 
                                bg = BG_MAIN)
        self.plotFrame_button.grid(column = 0, row=0, sticky=N+S+E+W)
        #self.plotFrame.pack(fill = Y, side = LEFT, expand = True)

        # GRID PLOT FRAME
        self.plotFrame_button.grid_rowconfigure(0, weight =1)

        self.plotbutton = []
        for n in range(NR_PLOT):
            self.plotFrame_button.grid_columnconfigure(n, weight =1)
            self.plotbutton.append( Radiobutton( self.plotFrame_button, 
                                                 text= PLOT_NAMES[n], 
                                                 value = n, 
                                                 variable = self.plot_select, 
                                                 command = self.plot_change,
                                                 bg = BG_SUB, 
                                                 fg=FG_TEXT,
                                                 selectcolor = BG_CHECK,
                                                 highlightbackground = BG_SUB) )    
            self.plotbutton[n].grid(column = n, row = 0, sticky= N+S+E+W)
        #self.plot_select.set(0)

        # ADD CANVAS TO FRAME
        self.plotFrame_plot = Frame( self.plotFrame, 
                                bd=0, 
                                bg = BG_MAIN)
        self.plotFrame_plot.grid(column = 0, row=1, sticky=N+S+E+W)
        self.plotFrame_plot.grid_columnconfigure(0, weight =1)
        self.plotFrame_plot.grid_rowconfigure(0, weight =1)

        self.plot_canvas = FigureCanvasTkAgg(f, self.plotFrame_plot)
        self.plot_canvas.get_tk_widget().grid(column = 0, row=0, sticky=N+S+E+W)  


    # D I R E C T   C O N T R O L   F R A M E
        # CREATE DIRECT CONTROL FRAME
        self.dicoFrame = Frame( self.contentFrame, 
                                bd      =2, 
                                relief  = SUNKEN, 
                                bg      = BG_MAIN)
        self.dicoFrame.grid(column = 1, row=0, sticky=N+S+E+W)
        #self.dicoFrame.pack(fill = BOTH, side = RIGHT, expand = True)

        # GRID DIRECTO CONTROL FRAME
        self.dicoFrame.grid_columnconfigure(0,weight=1)
        self.dicoFrame.grid_rowconfigure(0,weight=1)
        self.dicoFrame.grid_rowconfigure(1,weight=1)
        self.dicoFrame.grid_rowconfigure(2,weight=1)

    #   - L I V E   S T A T U S   F R A M E
        # ADD LIVE STATUS FRAME TO DICO FRAME
        self.live_frame = Frame( self.dicoFrame, 
                                 bd=1, 
                                 relief= SUNKEN, 
                                 bg = BG_SUB)
        self.live_frame.grid_columnconfigure(0, weight =1)
        # self.live_frame.grid_columnconfigure(1, weight =1)
        self.live_frame.grid_rowconfigure(0, weight =1)
        self.live_frame.grid_rowconfigure(1, weight =1)
        self.live_frame.grid_rowconfigure(2, weight =2)

        #self.live_frame.pack(fill = BOTH, side = TOP, expand = True)
        self.live_frame.grid(column = 0, row=0, sticky=N+S+E+W)

        self.live_header_frame = Frame( self.live_frame, 
                                        bg = BG_MAIN)
        self.live_header_frame.grid(column = 0, row=0, sticky=N+S+E+W)
        self.live_header_frame.grid_rowconfigure(0, weight =1)

        self.live_content_frame = Frame( self.live_frame, 
                                         bg = BG_SUB)
        self.live_content_frame.grid(column = 0, row=1, sticky=N+S+E+W)
        self.live_content_frame.grid_columnconfigure(0, weight =1)


        self.live_label = Label( self.live_header_frame, 
                                 text = "~ L I V E   M O N I T O R", 
                                 bg = BG_SUB, 
                                 fg = FG_TEXT)
        self.live_label.grid(column = 0, row = 0, sticky = N+S+W)

        self.live_content_frame.grid_rowconfigure(0, weight =2)
        self.live_top_padding = Label(  self.live_content_frame, 
                                        text = "", 
                                        bg = BG_SUB, 
                                        fg = FG_TEXT)
        self.live_top_padding.grid(column = 0, row = 0, columnspan = 2, sticky = N+S+W)

        self.color_index = 0
        self.color_toggle = [BG_TOG_A,BG_TOG_B]
        self.live_heat_frame = []
        self.live_heat_label = []
        self.live_heat_pad =[]
        self.live_heat_value = []
        self.live_heat_unit = []
        for n in range(NR_THERMO):
            tmp = NAMES_THERMO[n] + " :   "
            row_nr = (self.color_index+1)
            self.live_content_frame.grid_rowconfigure(row_nr, weight =3)

            self.live_heat_frame.append( Frame( self.live_content_frame, 
                                                bg = self.color_toggle[self.color_index % 2]) )
            self.live_heat_frame[n].grid(column = 0, row= row_nr, sticky=N+S+W+E)
            self.live_heat_frame[n].grid_rowconfigure(0, weight =1)
            self.live_heat_frame[n].grid_columnconfigure(0, weight =1)
            self.live_heat_frame[n].grid_columnconfigure(1, weight =2)
            self.live_heat_frame[n].grid_columnconfigure(2, weight =1)
            self.live_heat_frame[n].grid_columnconfigure(3, weight =0)

            self.live_heat_label.append( Label( self.live_heat_frame[n], 
                                                text = tmp, 
                                                bg = self.color_toggle[self.color_index % 2], 
                                                fg = FG_TEXT ))
            self.live_heat_label[n].grid(column = 0, row= 0, sticky=N+S+W)
            #self.live_heat_pad.append(Label(self.live_heat_frame[n], text = "", bg = self.color_toggle[self.color_index % 2], fg = FG_TEXT ))
            #self.live_heat_pad[n].grid(column = 1, row= 0, sticky=N+S+W+E)

            self.live_heat_value.append( Label( self.live_heat_frame[n], 
                                                textvariab = self.temperature_var[n], 
                                                bg = self.color_toggle[self.color_index % 2], 
                                                fg = FG_TEXT) )
            self.live_heat_value[n].grid(column = 2, row= 0, sticky=N+S+E)

            self.live_heat_unit.append( Label(  self.live_heat_frame[n], 
                                                text = UNIT_THERMO, 
                                                bg = self.color_toggle[self.color_index % 2], 
                                                fg = FG_TEXT ) )
            self.live_heat_unit[n].grid(column = 3, row= 0, sticky=N+S+E)
            self.color_index = self.color_index + 1
            
        self.live_moist_frame = []
        self.live_moist_label = []
        self.live_moist_value = []
        self.live_moist_pad =[]
        self.live_moist_unit = []
        for n in range(NR_MOISTURE):
            tmp = NAMES_MOISTURE[n] + "  :   "
            row_nr = (self.color_index+1)
            self.live_content_frame.grid_rowconfigure(row_nr, weight =3)

            self.live_moist_frame.append( Frame( self.live_content_frame, 
                                                 bg = self.color_toggle[self.color_index % 2] ) )
            self.live_moist_frame[n].grid(column = 0, row= row_nr, sticky=N+S+W+E)
            self.live_moist_frame[n].grid_rowconfigure(0, weight =1)
            self.live_moist_frame[n].grid_columnconfigure(0, weight =1)
            self.live_moist_frame[n].grid_columnconfigure(1, weight =2)
            self.live_moist_frame[n].grid_columnconfigure(2, weight =1)
            self.live_moist_frame[n].grid_columnconfigure(3, weight =0)

            self.live_moist_label.append( Label( self.live_moist_frame[n], 
                                                 text = tmp, 
                                                 bg = self.color_toggle[self.color_index % 2], 
                                                 fg = FG_TEXT ) )
            self.live_moist_label[n].grid(column = 0, row= 0, sticky=N+S+W)
            #self.live_moist_pad.append(Label(self.live_moist_frame[n], text = "", bg = self.color_toggle[self.color_index % 2], fg = FG_TEXT ))
            #self.live_moist_pad[n].grid(column = 1, row= 0, sticky=N+S+W+E)
            self.live_moist_value.append( Label( self.live_moist_frame[n], 
                                                 textvariab = self.moisture_var[n], 
                                                 bg = self.color_toggle[self.color_index % 2], 
                                                 fg = FG_TEXT ) )
            self.live_moist_value[n].grid(column = 2, row= 0, sticky=N+S+E)
            self.live_moist_unit.append( Label( self.live_moist_frame[n], 
                                                text = UNIT_MOISTURE, 
                                                bg = self.color_toggle[self.color_index % 2], 
                                                fg = FG_TEXT ) )
            self.live_moist_unit[n].grid(column = 3, row= 0, sticky=N+S+E)
            self.color_index = self.color_index + 1
            
        row_nr = (self.color_index+1)
        self.live_content_frame.grid_rowconfigure(0, weight =2)
        self.live_bottom_padding = Label(   self.live_content_frame, 
                                            text = "", bg = BG_SUB, 
                                            fg = FG_TEXT )
        self.live_bottom_padding.grid(column = 0, row = row_nr, columnspan = 2, sticky = N+S+W)

    #   - M A I N    D I C O   N O T E B O O K   F R A M E
        self.dicoFrame_notebook_frame = Frame( self.dicoFrame, 
                                            bg = BG_MAIN)
        self.dicoFrame_notebook_frame.grid(column = 0, row=1, sticky=N+S+E+W)

        self.dicoFrame_notebook_frame.grid_columnconfigure(0,weight=1)
        self.dicoFrame_notebook_frame.grid_rowconfigure(0,weight=1)

        self.dicoFrame_notebook = ttk.Notebook(self.dicoFrame_notebook_frame) #, width = 300)
        self.dicoFrame_notebook.grid(column = 0, row=0, sticky=N+S+E+W)

    #   - S E R I A L  F R A M E     DICONB
        # CREATE SERIAL FRAME IN DICO FRAME
        self.serial_frame = Frame(  self.dicoFrame_notebook, 
                                    bd      = 1, 
                                    bg      = BG_MAIN, 
                                    relief  = SUNKEN)
        self.dicoFrame_notebook.add(self.serial_frame, text = 'SERIAL')
        #self.serial_frame.grid(column = 0, row=0, sticky=N+S+E+W)
        #self.serial_frame.pack(side = TOP, fill = Y, expand = True)

        # GRID SERIAL FRAME
        self.serial_frame.grid_columnconfigure(0,weight=1)
        self.serial_frame.grid_rowconfigure(0,weight=0)
        self.serial_frame.grid_rowconfigure(1,weight=1)

        # ADD HEADER TEXT
        self.serial_header_frame = Frame(   self.serial_frame, 
                                            bg = BG_MAIN)
        self.serial_header_frame.grid(column = 0, row=0, sticky=N+S+E+W)
        self.serial_header_frame.grid_columnconfigure(0,weight=1)

        self.serial_header_label = Label(   self.serial_header_frame, 
                                            text = "~  S E R I A L ", 
                                            bg   = BG_MAIN, 
                                            fg   = FG_TEXT)
        self.serial_header_label.grid(column = 0, row=0, sticky=N+S+W)

        # ADD NOTEBOOK TO SERIAL FRAME
        self.serial_notebook_frame = Frame( self.serial_frame, 
                                            bg = BG_MAIN)
        self.serial_notebook_frame.grid(column = 0, row=1, sticky=N+S+E+W)
        self.serial_notebook_frame.grid_columnconfigure(0,weight=1)
        self.serial_notebook_frame.grid_rowconfigure(0,weight=1)

        self.serial_notebook = ttk.Notebook(self.serial_notebook_frame) #, width = 300)
        self.serial_notebook.grid(column = 0, row=0, sticky=N+S+E+W)

        # CREATE CONNECTION FRAME IN NOTEBOOK
        self.serial_connectionFrame = Frame( self.serial_notebook, 
                                             bg = BG_SUB)
        self.serial_connectionFrame.grid_columnconfigure(0,weight=1)
        self.serial_connectionFrame.grid_columnconfigure(1,weight=1)
        self.serial_connectionFrame.grid_rowconfigure(0,weight=1)
        self.serial_connectionFrame.grid_rowconfigure(1,weight=0)
        self.serial_connectionFrame.grid_rowconfigure(2,weight=0)
        self.serial_connectionFrame.grid_rowconfigure(3,weight=0)
        self.serial_connectionFrame.grid_rowconfigure(4,weight=1)
        self.serial_connectionFrame.grid_rowconfigure(5,weight=8)
        self.serial_notebook.add(self.serial_connectionFrame, text = 'connect')
        
        # ADD COMBOBOX
        self.serial_combo_port = ttk.Combobox( self.serial_connectionFrame,
                                          values = self.serial_combo_list,
                                          postcommand = self.postcom_port_list)
        self.serial_combo_port.grid(column = 0, row=1, columnspan = 2, sticky=N+S+E+W)

        # ADD ENTRY FOR PORT TO CONNECTION FRAME
        self.serial_entry_port = Entry( self.serial_connectionFrame, 
                                        textvariable        = self.serial_var_port, 
                                        highlightbackground = BG_SUB, 
                                        selectforeground    = 'black',
                                        bg                  = BG_ENTRY, 
                                        fg                  = FG_ENTRY )
        self.serial_entry_port.grid(column = 0, row=2, columnspan = 2, sticky=N+S+E+W)

        # ADD OPEN CONNECTION BUTTON TO CONNECTION FRAME
        self.serial_button_open= Button(    self.serial_connectionFrame, 
                                            text    = "open", 
                                            command = self.open_serial_connection)
        self.serial_button_open.grid(column = 0, row =3, sticky=N+S+E+W)

        self.serial_button_close = Button(  self.serial_connectionFrame,
                                            text    = "close", 
                                            command = self.close_serial_connection)
        self.serial_button_close.grid(column = 1, row=3, sticky=N+S+E+W)


        # ADD LABEL FOR STATUS TO CONNECTION FRAME
        self.serial_label_status = Label(   self.serial_connectionFrame, 
                                            textvariable = self.serial_connection_string, 
                                            bg           = BG_SUB, 
                                            fg           = FG_TEXT)
        self.serial_label_status.grid(column = 0, row=4, columnspan = 2, sticky=N+S+E+W)




        self.postcom_port_list()    # call post command to have initial value in list
        # SERIAL NOTEBOOK _ DIRECT INTERFACE
        self.serial_interfaceFrame = Frame( self.serial_notebook, 
                                            bg = BG_SUB)    
        self.serial_notebook.add(self.serial_interfaceFrame, text = 'comm')
        self.serial_interfaceFrame.grid_columnconfigure(0,weight=1)
        self.serial_interfaceFrame.grid_columnconfigure(1,weight=1)
        self.serial_interfaceFrame.grid_rowconfigure(0,weight=1)
        self.serial_interfaceFrame.grid_rowconfigure(1,weight=0)
        self.serial_interfaceFrame.grid_rowconfigure(2,weight=0)
        self.serial_interfaceFrame.grid_rowconfigure(3,weight=1)
        self.serial_interfaceFrame.grid_rowconfigure(4,weight=8)

        self.serial_entry_command = Entry(  self.serial_interfaceFrame, 
                                            textvariable        = self.serial_var_string,  
                                            highlightbackground = BG_SUB, 
                                            selectforeground    = 'black',
                                            bg                  = BG_ENTRY, 
                                            fg                  = FG_ENTRY)
        self.serial_entry_command.grid(column = 0, row=1, columnspan = 2, sticky=N+S+E+W)

        # ADD LABEL FOR STATUS TO CONNECTION FRAME
        self.serial_button_read= Button(    self.serial_interfaceFrame, 
                                            text    = "read", 
                                            command = self.read_serial_string)
        self.serial_button_read.grid(column = 0, row=2, sticky=N+S+E+W)

        self.serial_button_write= Button(   self.serial_interfaceFrame, 
                                            text    = "write", 
                                            command = self.write_serial_string)
        self.serial_button_write.grid(column = 1, row=2, sticky=N+S+E+W)

        self.serial_entry_label = Label(    self.serial_interfaceFrame, 
                                            textvariable = self.serial_entry_string, 
                                            bg           = BG_SUB, 
                                            fg           = FG_TEXT)
        self.serial_entry_label.grid(column = 0, row=3, columnspan = 2, sticky=N+S+E+W)



    #   - D E V I C E  C O N T R O L   F R A M E    DICONB
        # ADD DEVICE CONTROL TO DICOFRAME
        self.devco_frame = Frame( self.dicoFrame_notebook, 
                                  bd=1, 
                                  relief = SUNKEN, 
                                  bg = BG_MAIN)
        #self.devco_frame.pack(fill = Y, side = TOP, expand = True)
        #self.devco_frame.grid(column = 0, row=2, sticky=N+S+E+W)
        self.dicoFrame_notebook.add(self.devco_frame, text = 'DEVICES')
        self.devco_frame.grid_columnconfigure(0,weight=1)
        self.devco_frame.grid_rowconfigure(0,weight=0)
        self.devco_frame.grid_rowconfigure(1,weight=1)

        # DEVICE CONTROL HEADER TEXT
        self.devco_label = Label( self.devco_frame, 
                                  text= "~  D E V I C E  C O N T R O L ", 
                                  bg = BG_MAIN, 
                                  fg = FG_TEXT )
        self.devco_label.grid(column = 0, row=0, sticky=N+S+W)

    #   - D E V I C E  C O N T R O L   N O T E B O O K    DICONB
        self.devco_notebook = ttk.Notebook(self.devco_frame) #, width = 300
        self.devco_notebook.grid(column = 0, row=1, sticky=N+S+E+W)

    #   -    L A M P   F R A M E    DEVCONB DICONB
        self.devco_lamp_frame = Frame(  self.devco_notebook, 
                                        bd=1, 
                                        relief = SUNKEN, 
                                        bg = BG_MAIN)
        self.devco_lamp_frame.grid_rowconfigure(0, weight =1)
        self.devco_lamp_frame.grid_rowconfigure(1, weight =1)

        self.devco_notebook.add(self.devco_lamp_frame, text = 'LIGHT', sticky=N+S+E+W)
        
        self.devco_lamp_notebook = ttk.Notebook(self.devco_lamp_frame)
        self.devco_lamp_notebook.pack(side=TOP , fill = BOTH)

        self.devco_label_lampName = []
        self.devco_label_lampState = []
        self.devco_label_slider= []
        self.devco_slider_lamp=[]
        self.devco_button_lampOff=[]
        self.devco_button_lampOn=[]
        self.devco_lamp_direct_frame=[]
        for n in range(NR_LAMP):
            self.devco_lamp_direct_frame.append( Frame( self.devco_lamp_frame, 
                                                        bg = BG_SUB) )
            self.devco_lamp_notebook.add(self.devco_lamp_direct_frame[n], text = NAMES_LAMP[n], sticky =N+S+E+W)
            self.devco_lamp_direct_frame[n].grid_columnconfigure(0, weight =1)
            self.devco_lamp_direct_frame[n].grid_rowconfigure(0, weight =0)
            self.devco_lamp_direct_frame[n].grid_rowconfigure(1, weight =1)
            self.devco_lamp_direct_frame[n].grid_rowconfigure(2, weight =1)
            self.devco_lamp_direct_frame[n].grid_rowconfigure(3, weight =2)
            # LAMP STATE
            self.devco_lamp_state_frame = Frame( self.devco_lamp_direct_frame[n], 
                                                 bg = BG_SUB)
            self.devco_lamp_state_frame.grid(column = 0, row = 0, sticky = N+S+E+W)
            self.devco_lamp_state_frame.grid_columnconfigure(0, weight =1)
            self.devco_lamp_state_frame.grid_columnconfigure(0, weight =1)
            self.devco_lamp_state_frame.grid_rowconfigure(0, weight =0)

            self.devco_label_lampName.append( Label( self.devco_lamp_state_frame, 
                                                     text = NAMES_LAMP[n], 
                                                     bg = BG_SUB, 
                                                     fg = FG_TEXT) )
            self.devco_label_lampName[n].grid(column = 0, row = 0, sticky = N+S+W)

            self.devco_label_lampState.append( Label( self.devco_lamp_state_frame, 
                                                      textvariable = self.lamp_state[n], 
                                                      bg = BG_SUB, 
                                                      fg = FG_TEXT) )
            self.devco_label_lampState[n].grid(column = 1, row =0, sticky = N+S+E+W)

            tmp0 = []
            tmp1 = []
            self.devco_lamp_slider_frame = Frame( self.devco_lamp_direct_frame[n], 
                                                  bg = BG_SUB)
            self.devco_lamp_slider_frame.grid(column = 0, row = 1, sticky = N+S+E+W)
            self.devco_lamp_slider_frame.grid_columnconfigure(0, weight =1)
            self.devco_lamp_slider_frame.grid_columnconfigure(1, weight =2)
            

            for m in range(len(CHANNELS_LAMP[n])):
                # SLIDER LABELS
                tmp0.append( Label( self.devco_lamp_slider_frame, 
                                    text = (CHANNELS_LAMP[n][m] + "-channel"), 
                                    bg = BG_SUB, 
                                    fg = FG_TEXT) )

                tmp1.append( Scale( self.devco_lamp_slider_frame, 
                                    orient = HORIZONTAL, 
                                    variable = self.lamp_output[n][m], 
                                    command = self.update_lamp, 
                                    to = 255, 
                                    bg = BG_SUB, 
                                    highlightbackground = BG_SUB,
                                    fg = FG_TEXT) )

            self.devco_label_slider.append(tmp0)
            self.devco_slider_lamp.append(tmp1)   

            for m in range(len(CHANNELS_LAMP[n])):
                # SLIDERS
                self.devco_lamp_slider_frame.grid_rowconfigure(m, weight =0)
                self.devco_label_slider[n][m].grid(column = 0, row = m, sticky=S+W)
                self.devco_slider_lamp[n][m].grid(column = 1, row = m, columnspan = 3, sticky=S+W+N+E)

            self.devco_lamp_switch_frame = Frame( self.devco_lamp_direct_frame[n], 
                                                  bg = BG_SUB)
            self.devco_lamp_switch_frame.grid(column = 0, row = 2, sticky = N+S+E+W)
            self.devco_lamp_switch_frame.grid_columnconfigure(0, weight =1)
            self.devco_lamp_switch_frame.grid_columnconfigure(1, weight =1)
            self.devco_lamp_switch_frame.grid_rowconfigure(0, weight =0)

            # ON BUTTON
            self.devco_button_lampOff.append( Button(self.devco_lamp_switch_frame, text= "OFF", command = self.disable_lamp))
            self.devco_button_lampOff[n].grid(column = 0, row = 0, sticky=N+S+E+W)

            # OFF BUTTON
            self.devco_button_lampOn.append( Button(self.devco_lamp_switch_frame, text= "ON", command = self.enable_lamp))
            self.devco_button_lampOn[n].grid(column = 1,  row = 0, sticky=N+S+E+W)

        # AUTOMATIC LIGHT MODE
        self.devco_lamp_daylight_frame = Frame( self.devco_lamp_frame, 
                                                bg = BG_MAIN)
        self.devco_lamp_daylight_frame.pack(side=TOP , fill = BOTH)
        self.devco_lamp_daylight_frame.grid_columnconfigure(0, weight =1)
        self.devco_lamp_daylight_frame.grid_columnconfigure(1, weight =1)
        self.devco_lamp_daylight_frame.grid_columnconfigure(2, weight =0)
        self.devco_lamp_daylight_frame.grid_columnconfigure(3, weight =0)
        self.devco_lamp_daylight_frame.grid_columnconfigure(4, weight =0)

        self.devco_daylight_toggle = Checkbutton( self.devco_lamp_daylight_frame, 
                                                  text = "Toggle automatic daylight mode", 
                                                  variable = self.enable_daylight, 
                                                  onvalue = 1, 
                                                  offvalue =0, 
                                                  command = self.update_daylight_params, 
                                                  bg = BG_MAIN, 
                                                  fg = FG_TEXT,
                                                  highlightbackground = BG_SUB,
                                                  selectcolor = BG_CHECK)
        self.devco_daylight_toggle.grid(column = 0, row = 1, columnspan = 5, sticky=S+W+N+E)

        self.devco_daylight_status = Label( self.devco_lamp_daylight_frame, 
                                            textvariable = self.daylight_status, 
                                            bg = BG_MAIN, 
                                            fg = FG_TEXT)
        self.devco_daylight_status.grid(column = 0, row = 2, columnspan = 5, sticky=S+W+N+E)

        self.devco_daylight_start_label = Label( self.devco_lamp_daylight_frame, 
                                                 text = "Day start", 
                                                 bg = BG_MAIN, 
                                                 fg = FG_TEXT)
        self.devco_daylight_start_label.grid(column = 0, row = 3, columnspan = 1, sticky=S+W+N)

        self.devco_daylight_start_hour = Entry( self.devco_lamp_daylight_frame, 
                                                textvariable = self.daylight_tv_start_hour, 
                                                width = 3, 
                                                bg = BG_ENTRY, 
                                                fg = FG_ENTRY, 
                                                highlightbackground = BG_MAIN)
        self.devco_daylight_start_hour.grid(column = 2, row = 3, sticky=S+E+N)

        self.devco_daylight_start_sep = Label( self.devco_lamp_daylight_frame, 
                                                 text = " : ", 
                                                 bg = BG_MAIN, 
                                                 fg = FG_TEXT)
        self.devco_daylight_start_sep.grid(column = 3, row = 3, columnspan = 1, sticky=S+E+W+N)

        self.devco_daylight_start_minute = Entry( self.devco_lamp_daylight_frame, 
                                                  textvariable = self.daylight_tv_start_min, 
                                                  width =3, 
                                                  bg =BG_ENTRY, 
                                                  fg = FG_ENTRY, 
                                                  highlightbackground = BG_MAIN)
        self.devco_daylight_start_minute.grid(column = 4, row = 3, sticky=S+W+N)

        self.devco_daylight_end_label = Label( self.devco_lamp_daylight_frame, 
                                               text = "Day end", 
                                               bg = BG_MAIN, 
                                               fg = FG_TEXT)
        self.devco_daylight_end_label.grid(column = 0, row = 4, columnspan = 1, sticky=S+W+N)

        self.devco_daylight_end_hour = Entry( self.devco_lamp_daylight_frame, 
                                              textvariable = self.daylight_tv_end_hour, 
                                              width = 3, 
                                              bg = BG_ENTRY, 
                                              fg = FG_ENTRY, 
                                              highlightbackground = BG_MAIN)
        self.devco_daylight_end_hour.grid(column = 2, row = 4)

        self.devco_daylight_end_sep = Label( self.devco_lamp_daylight_frame, 
                                                 text = " : ", 
                                                 bg = BG_MAIN, 
                                                 fg = FG_TEXT)
        self.devco_daylight_end_sep.grid(column = 3, row = 4, columnspan = 1, sticky=S+E+W+N)

        self.devco_daylight_end_minute = Entry( self.devco_lamp_daylight_frame, 
                                                textvariable = self.daylight_tv_end_min, 
                                                width = 3, 
                                                bg = BG_ENTRY, 
                                                fg = FG_ENTRY, 
                                                highlightbackground = BG_MAIN)
        self.devco_daylight_end_minute.grid(column = 4, row = 4)

        self.devco_daylight_ramp_label = Label( self.devco_lamp_daylight_frame, 
                                                text = "Sunrise/set period", 
                                                bg = BG_MAIN, 
                                                fg = FG_TEXT)
        self.devco_daylight_ramp_label.grid(column = 0, row = 5, columnspan = 1, sticky=S+W+N)

        self.devco_daylight_ramp_hour = Entry(  self.devco_lamp_daylight_frame, 
                                                textvariable = self.daylight_tv_ramp_hour,
                                                validate = "all", 
                                                validatecommand = self.update_daylight_params, 
                                                width =3, 
                                                bg=BG_ENTRY, 
                                                fg = FG_ENTRY, 
                                                highlightbackground = BG_MAIN)
        self.devco_daylight_ramp_hour.grid(column = 2, row = 5)

        self.devco_daylight_ramp_sep = Label( self.devco_lamp_daylight_frame, 
                                         text = " : ", 
                                         bg = BG_MAIN, 
                                         fg = FG_TEXT)
        self.devco_daylight_ramp_sep.grid(column = 3, row = 5, columnspan = 1, sticky=S+E+W+N)

        self.devco_daylight_ramp_minute = Entry( self.devco_lamp_daylight_frame, 
                                                 textvariable = self.daylight_tv_ramp_min,
                                                 validate = "all", 
                                                 validatecommand = self.update_daylight_params, 
                                                 width =3, bg=BG_ENTRY, 
                                                 fg = FG_ENTRY, 
                                                 highlightbackground = BG_MAIN)
        self.devco_daylight_ramp_minute.grid(column = 4, row = 5)

        self.devco_daylight_brightness_label = Label( self.devco_lamp_daylight_frame, 
                                                      text = "Full brightness", 
                                                      bg=BG_MAIN, 
                                                      fg = FG_TEXT)
        self.devco_daylight_brightness_label.grid(column = 0, row = 6, columnspan = 1, sticky=S+W+N)
        self.devco_daylight_brightness_value = Entry( self.devco_lamp_daylight_frame, 
                                                      textvariable = self.daylight_brightness, 
                                                      width =3, 
                                                      bg=BG_ENTRY, 
                                                      fg = FG_ENTRY, 
                                                      highlightbackground = BG_MAIN)
        self.devco_daylight_brightness_value.grid(column = 4, row = 6)

    #   -    H Y D R O L I C S   F R A M E    DEVCONB DICONB
        self.devco_hydro_frame = Frame( self.devco_notebook, 
                                        bg = BG_SUB)
        self.devco_hydro_frame.grid_columnconfigure(0, weight =1)
        self.devco_hydro_frame.grid_rowconfigure(0, weight =0)
        self.devco_hydro_frame.grid_rowconfigure(1, weight =1)
        self.devco_notebook.add(self.devco_hydro_frame, text = 'HYDROLICS', sticky=N+S+E+W)


        # PUMP FRAME 
        self.devco_hydro_pump_frame = Frame( self.devco_hydro_frame, 
                                        bg = BG_SUB,
                                        bd = 2,
                                        relief = SUNKEN )
        self.devco_hydro_pump_frame.grid(column = 0, row = 0, sticky=S+W+N+E)   

        self.devco_hydro_pump_frame.grid_columnconfigure(0, weight =1)
        self.devco_hydro_pump_frame.grid_columnconfigure(1, weight =1)
        self.devco_hydro_pump_frame.grid_rowconfigure(0, weight =0)
        self.devco_hydro_pump_frame.grid_rowconfigure(1, weight =0)
        self.devco_hydro_pump_frame.grid_rowconfigure(2, weight =0)
        self.devco_hydro_pump_frame.grid_rowconfigure(3, weight =0)


        # PUMP RUNNING FB
        self.devco_label_pumpRunning = Label( self.devco_hydro_pump_frame, 
                                              textvariable = self.pump_state[0], 
                                              bg = BG_SUB, 
                                              fg = FG_TEXT)
        self.devco_label_pumpRunning.grid(column = 0, row = 0, columnspan = 2, sticky=S+W+N+E)

        # PUMP SLIDER
        self.devco_slider_pumpValue = Scale( self.devco_hydro_pump_frame, 
                                             orient = HORIZONTAL, 
                                             command = self.update_pump, 
                                             to = 255, 
                                             bg = BG_SUB, 
                                             highlightbackground = BG_SUB,
                                             fg=FG_TEXT)
        self.devco_slider_pumpValue.grid(column = 0, row = 1, columnspan = 2, sticky=S+W+N+E)

        # TOGGLE PUMP STATE
        self.devco_button_pumpEnable = Button(  self.devco_hydro_pump_frame, 
                                                command = self.set_pumpEnable, 
                                                text = "Enable pump")
        self.devco_button_pumpEnable.grid(column = 0, row = 2, sticky=S+W+N+E)

        self.devco_button_pumpDisable = Button( self.devco_hydro_pump_frame, 
                                                command = self.set_pumpDisable, 
                                                text = "Disable pump")
        self.devco_button_pumpDisable.grid(column = 1, row = 2, sticky=S+W+N+E)

        self.devco_check_overrule_pump = Checkbutton( self.devco_hydro_pump_frame, 
                                                      variable = self.overrule_pump_interlock[0], 
                                                      onvalue= 1, 
                                                      offvalue=0, 
                                                      command = self.toggle_pump_interlock,
                                                      text = "Overrule Pump Interlock", 
                                                      bg = BG_SUB,
                                                      highlightbackground = BG_SUB,
                                                      fg=FG_TEXT,
                                                      selectcolor = BG_CHECK,)
        self.devco_check_overrule_pump.grid(column = 0, row = 3, columnspan = 2, sticky=S+W+N+E)


        # FLOW FRAME 
        self.devco_hydro_flow_frame = Frame( self.devco_hydro_frame, 
                                        bg = BG_SUB,
                                        bd = 2,
                                        relief = SUNKEN)
        self.devco_hydro_flow_frame.grid(column = 0, row = 1, sticky=S+W+N+E)

        self.devco_hydro_flow_frame.grid_columnconfigure(0, weight =1)
        self.devco_flow=[]
        for n in range(NR_FLOW):
            self.devco_hydro_flow_frame.grid_rowconfigure(n, weight =1)

            # TOGGLE COLOURS
            if n%2 == 0:
                self.devco_flow.append( Radiobutton( self.devco_hydro_flow_frame, 
                                                     text= NAMES_FLOW[n], 
                                                     value = n, 
                                                     variable = self.flow_state, 
                                                     command = self.set_flow_circuit, 
                                                     bg = BG_TOG_A, 
                                                     fg=FG_TEXT,
                                                     anchor = W,
                                                     activeforeground = FG_TEXT2,
                                                     activebackground = BG_SEL,
                                                     highlightbackground = BG_TOG_A,
                                                     selectcolor = BG_TOG_A) )
            else:
                self.devco_flow.append( Radiobutton( self.devco_hydro_flow_frame, 
                                         text= NAMES_FLOW[n], 
                                         value = n, 
                                         variable = self.flow_state, 
                                         command = self.set_flow_circuit, 
                                         bg = BG_TOG_B, 
                                         fg=FG_TEXT,
                                         anchor = W,
                                         activeforeground = FG_TEXT2,
                                         activebackground = BG_SEL,
                                         highlightbackground = BG_TOG_B,
                                         selectcolor = BG_TOG_B) )
            self.devco_flow[n].grid(column = 0, row = n, sticky=S+W+N+E)


        # ADD LAST RADIO
        self.devco_hydro_flow_frame.grid_rowconfigure(NR_FLOW, weight =1)
        if NR_FLOW%2 == 0:
            self.devco_flow.append( Radiobutton( self.devco_hydro_flow_frame, 
                                                 text= "DISABLED", 
                                                 value = NR_FLOW, 
                                                 variable = self.flow_state, 
                                                 command = self.set_flow_circuit, 
                                                 bg = BG_TOG_A,
                                                 fg=FG_TEXT,
                                                 anchor = W,
                                                 activeforeground = FG_TEXT2,
                                                 activebackground = BG_SEL,
                                                 highlightbackground = BG_TOG_A,
                                                 selectcolor = BG_TOG_A) )
        else:
            self.devco_flow.append( Radiobutton( self.devco_hydro_flow_frame, 
                                         text= "DISABLED", 
                                         value = NR_FLOW, 
                                         variable = self.flow_state, 
                                         command = self.set_flow_circuit, 
                                         bg = BG_TOG_B,
                                         fg=FG_TEXT,
                                         anchor = W,
                                         activeforeground = FG_TEXT2,
                                         activebackground = BG_SEL,
                                         highlightbackground = BG_TOG_B,
                                         selectcolor = BG_TOG_B) )
        self.devco_flow[NR_FLOW].grid(column = 0, row = (NR_FLOW), sticky=S+W+N+E)

    #   -    R E L A Y  F R A M E    DEVCONB DICONB
        self.devco_relay_frame = Frame( self.devco_notebook, 
                                        bg = BG_SUB)
        self.devco_notebook.add(self.devco_relay_frame, text = 'RELAYS', sticky=N+S+E+W)

        self.devco_relay_frame.grid_columnconfigure(0, weight =1)
        self.devco_relay = []
        for n in range(NR_RELAY):
            self.devco_relay_frame.grid_rowconfigure(n, weight =1)
            if n%2 == 0:
                self.devco_relay.append( Checkbutton( self.devco_relay_frame, 
                                      text= NAMES_RELAY[n], 
                                      variable = self.enable_relay[n], 
                                      onvalue= 1, 
                                      offvalue=0, 
                                      command = self.toggle_relay, 
                                      bg = BG_TOG_A,
                                      fg=FG_TEXT,
                                      anchor = W,
                                      activeforeground = FG_TEXT2,
                                      activebackground = BG_SEL,
                                      highlightbackground = BG_TOG_A,
                                      selectcolor = BG_TOG_B) )
            else:
                self.devco_relay.append( Checkbutton( self.devco_relay_frame, 
                                      text= NAMES_RELAY[n], 
                                      variable = self.enable_relay[n], 
                                      onvalue= 1, 
                                      offvalue=0, 
                                      command = self.toggle_relay, 
                                      bg = BG_TOG_B,
                                      fg=FG_TEXT,
                                      anchor = W,
                                      activeforeground = FG_TEXT2,
                                      activebackground = BG_SEL,
                                      highlightbackground = BG_TOG_B,
                                      selectcolor = BG_TOG_B) )

            self.devco_relay[n].grid(column = 0, row = n, columnspan = 4, sticky=S+W+N+E)

        # SET BACKGROUND CLOUR
        if DEBUG_MODE:
            self.configure(bg='red')
            self.mainframe.configure(bg='green')
            self.headerFrame.configure(bg='blue')
            self.contentFrame.configure(bg='yellow')
            self.plotFrame.configure(bg='orange')
            self.dicoFrame.configure(bg='magenta')

    #   - S C H E D U L E    F R A M E   DICONB 
        # shedule main frame
        self.schedule_frame = Frame(  self.dicoFrame_notebook, 
                                    bd      = 1, 
                                    bg      = BG_MAIN, 
                                    relief  = SUNKEN)
        self.dicoFrame_notebook.add(self.schedule_frame, text = 'SCHEDULER')
        self.schedule_frame.grid_columnconfigure(0,weight=1)
        self.schedule_frame.grid_columnconfigure(1,weight=1)
        self.schedule_frame.grid_columnconfigure(2,weight=1)
        self.schedule_frame.grid_columnconfigure(3,weight=1)
        self.schedule_frame.grid_columnconfigure(4,weight=1)
        self.schedule_frame.grid_rowconfigure(0,weight=1)

        # ADD SCHEDULER ROWS
        self.schedule_row_frame = []    # A FRAME FOR EACH ROW
        self.schedule_combo_dev = []    # DEVICE COMBO BOX
        self.schedule_combo_id = []     # DEVICE ID COMBOBOX
        self.schedule_entry_start = []
        self.schedule_entry_ontime = []
        self.schedule_entry_value = []

        # HEADER ROW
        self.schedule_lbl0 = Label(  self.schedule_frame, 
                            text    = "DEVICE", 
                            bg      = BG_MAIN, 
                            fg      = FG_TEXT, 
                            bd      = 0)
        self.schedule_lbl0.grid(column = 0, row=0, sticky=N+S+W+E)

        self.schedule_lbl1 = Label(  self.schedule_frame, 
                            text    = "ID", 
                            bg      = BG_MAIN, 
                            fg      = FG_TEXT, 
                            bd      = 0)
        self.schedule_lbl1.grid(column = 1, row=0, sticky=N+S+W+E)

        self.schedule_lbl2 = Label(  self.schedule_frame, 
                    text    = "START @", 
                    bg      = BG_MAIN, 
                    fg      = FG_TEXT, 
                    bd      = 0)
        self.schedule_lbl2.grid(column = 2, row=0, sticky=N+S+W+E)
        self.schedule_lbl3 = Label(  self.schedule_frame, 
                    text    = "ON TIME", 
                    bg      = BG_MAIN, 
                    fg      = FG_TEXT, 
                    bd      = 0)
        self.schedule_lbl3.grid(column = 3, row=0, sticky=N+S+W+E)
        self.schedule_lbl4 = Label(  self.schedule_frame, 
                    text    = "SP", 
                    bg      = BG_MAIN, 
                    fg      = FG_TEXT, 
                    bd      = 0)
        self.schedule_lbl4.grid(column = 4, row=0, sticky=N+S+W+E)

        # INFILL ROWS
        for n in range(len(self.schedule_sel)):
            self.schedule_frame.grid_rowconfigure(n+1 ,weight=0)   
            self.schedule_combo_dev.append(ttk.Combobox( self.schedule_frame,
                                          values = self.schedule_devices,
                                          postcommand = self.update_sched_combo_dev,
                                          width = 6) )
            self.schedule_combo_dev[n].grid(column = 0, row=n+1, sticky=N+S+E+W)
            self.schedule_combo_dev[n].current(0)

            self.schedule_combo_id.append(ttk.Combobox( self.schedule_frame,
                              values = ["-1"],
                              postcommand = self.update_sched_combo_id,
                              width = 3) )
            self.schedule_combo_id[n].grid(column = 1, row=n+1, sticky=N+S+E+W)
            self.schedule_combo_id[n].current(0)

            self.schedule_entry_start.append(Entry(  self.schedule_frame, 
                                                        textvariable        = self.schedule_var_start[n],  
                                                        highlightbackground = BG_SUB, 
                                                        selectforeground    = 'black',
                                                        bg                  = BG_ENTRY, 
                                                        fg                  = FG_ENTRY, 
                                                        width               = 8 ))
            self.schedule_entry_start[n].grid(column = 2, row=n+1, sticky=N+S+E+W)

            self.schedule_entry_ontime.append(Entry(  self.schedule_frame, 
                                                        textvariable        = self.schedule_var_ontime[n],  
                                                        highlightbackground = BG_SUB, 
                                                        selectforeground    = 'black',
                                                        bg                  = BG_ENTRY, 
                                                        fg                  = FG_ENTRY, 
                                                        width               = 4 ))
            self.schedule_entry_ontime[n].grid(column = 3, row=n+1, sticky=N+S+E+W)

            self.schedule_entry_value.append(Entry(  self.schedule_frame, 
                                                        textvariable        = self.schedule_var_value[n],  
                                                        highlightbackground = BG_SUB, 
                                                        selectforeground    = 'black',
                                                        bg                  = BG_ENTRY, 
                                                        fg                  = FG_ENTRY, 
                                                        width               = 3 ))
            self.schedule_entry_value[n].grid(column = 4, row=n+1, sticky=N+S+E+W)

        # FOOTER ROW
        self.schedule_frame.grid_rowconfigure(len(self.schedule_sel)+1 ,weight=8)   

#   PACK SELF
        self.grid_columnconfigure(0, weight =1)
        self.grid_rowconfigure(0, weight =1)
        self.pack(fill = BOTH, expand = True)

##   A N I M A T I O N
#  DEFINE MATPLOT FUIGURE
f, ax = pp.subplots(nrows = 4, ncols = 1)
f.set_tight_layout(True)
f.set_facecolor('#c4c4c4')
pp.tight_layout()


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    f.tight_layout()
warnings.filterwarnings("ignore",lineno=746, module="tkinter")
warnings.filterwarnings("ignore", category= UserWarning)

def update_plot():
    global BUFF_FILL, FIRST_SCAN, PLOT_WINDOW

    if not FIRST_SCAN and BUFF_FILL>0:
        if PLOT_WINDOW == 1:
            update_plot_light_temp()
        elif PLOT_WINDOW == 2:
            update_plot_pumping_water()
        else:
            update_plot_all()

def update_plot_all():
    global BUFF_FILL, FIRST_SCAN    
    global valM, valH, valH1, valP, valL
    global valMneat,valHneat, valH1neat, valPneat, valLneat

    my_time_list = get_time_list()
    my_label_list = get_label_list()
    my_tick_list = get_tick_list()
    my_clear_list = get_clear_list()

    ax[0].clear()
    ax[1].clear()
    ax[2].clear()
    ax[3].clear()

    ax[0].set_visible(True)
    ax[1].set_visible(True)
    ax[2].set_visible(True)
    ax[3].set_visible(True)

    ax[0].set_position([0.125, 0.81, 0.85, 0.17])
    ax[1].set_position([0.125, 0.59, 0.85, 0.17])
    ax[2].set_position([0.125, 0.37, 0.85, 0.17])
    ax[3].set_position([0.125, 0.15, 0.85, 0.17])

    #   F - UPDATE TEMOERATURE PLOT
    hy_min = min(min(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), min(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) - 1
    hy_max = max(max(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), max(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) + 1

    # SET X TICK TIME LABEL
    if BUFF_FILL > 1:
        ax[0].set_xticks(my_tick_list)
        ax[0].set_xticklabels(my_clear_list)

    ax[0].set_ylim([ hy_min, hy_max ])
    ax[0].set_ylabel("TC Temp [*C]")
    ax[0].grid(True)

    #   F - UPDATE LAMP
    hy_min = min(valLneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1
    hy_max = max(valLneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1


    # ax[1].set_ylim([ hy_min, hy_max ])
    ax[1].set_ylim(DEFAULT_RANGE_LAMP)
    ax[1].set_ylabel("LIGHT")   

    ax[1].grid(True)

        # SET X TICK TIME LABEL
    if BUFF_FILL > 1:
        ax[1].set_xticks(my_tick_list)
        ax[1].set_xticklabels(my_clear_list)

    #   F - UPDATE MOUSTURE PLOT
    hy_min = min(valMneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1
    hy_max = max(valMneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1


    ax[2].set_ylim([ hy_min, hy_max ])
    ax[2].set_ylabel("Moisture [%]")

    ax[2].grid(True)   

    # SET X TICK TIME LABEL
    if BUFF_FILL > 1:
        ax[2].set_xticks(my_tick_list)
        ax[2].set_xticklabels(my_clear_list)

    #   F - UPDATE PUMP
    hy_min = min(valPneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1
    hy_max = max(valPneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1
    

    ax[3].set_ylim([ hy_min, hy_max ])
    ax[3].set_ylabel("PUMP")

    ax[3].grid(True)

    # SET X TICK TIME LABEL
    if BUFF_FILL > 1:
        ax[3].set_xticks(my_tick_list)
        ax[3].set_xticklabels(my_label_list, rotation =45)

    #ax[3].set_xlabel("time [min]")

    f.set_tight_layout(True)    
    pp.tight_layout()

    ax[0].plot( valHneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valHneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='g' )
    ax[0].plot( valH1neat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valH1neat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='b' )
    ax[1].plot( valLneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valLneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )
    ax[2].plot( valMneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valMneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )
    ax[3].plot( valPneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valPneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )


def update_plot_light_temp():
    global BUFF_FILL, FIRST_SCAN    
    global valM, valH, valH1, valP, valL
    global valMneat,valHneat, valH1neat, valPneat, valLneat

    my_time_list = get_time_list()
    my_label_list = get_label_list()
    my_tick_list = get_tick_list()
    my_clear_list = get_clear_list()

    ax[0].clear()
    ax[1].clear()
    ax[2].clear()
    ax[3].clear()

    ax[0].set_visible(True)
    ax[1].set_visible(True)
    ax[2].set_visible(False)
    ax[3].set_visible(False)

    ax[0].set_position([0.15, 0.375, 0.8, 0.6])
    ax[1].set_position([0.15, 0.15, 0.8, 0.2])
    #ax[2].set_position([0.05, 0.05, 0.9, 0.3])
    #ax[3].set_position([0.05, 0.05, 0.9, 0.3])

    #   F - UPDATE TEMOERATURE PLOT
    hy_min = min(min(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), min(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) - 1
    hy_max = max(max(valHneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]), max(valH1neat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN])) + 1

    # SET X TICK TIME LABEL
    if BUFF_FILL > 1:
        ax[0].set_xticks(my_tick_list)
        ax[0].set_xticklabels(my_clear_list)

    ax[0].set_ylim([ hy_min, hy_max ])
    ax[0].set_ylabel("TC Temp [*C]")
    ax[0].grid(True)

    #   F - UPDATE LAMP
    hy_min = min(valLneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1
    hy_max = max(valLneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1

    # ax[1].set_ylim([ hy_min, hy_max ])
    ax[1].set_ylim(DEFAULT_RANGE_LAMP)
    ax[1].set_ylabel("LIGHT")   

    ax[1].grid(True)

        # SET X TICK TIME LABEL
    if BUFF_FILL > 1:
        ax[1].set_xticks(my_tick_list)
        ax[1].set_xticklabels(my_label_list, rotation =45)
    #ax[1].set_xlabel("time [min]")

    f.set_tight_layout(True)
    pp.tight_layout()

    ax[0].plot( valHneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valHneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='g' )
    ax[0].plot( valH1neat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valH1neat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ], color='b' )
    ax[1].plot( valLneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valLneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

def update_plot_pumping_water():
    global BUFF_FILL, FIRST_SCAN    
    global valM, valH, valH1, valP, valL
    global valMneat,valHneat, valH1neat, valPneat, valLneat

    my_time_list = get_time_list()
    my_label_list = get_label_list()
    my_tick_list = get_tick_list()
    my_clear_list = get_clear_list()

    ax[0].clear()
    ax[1].clear()
    ax[2].clear()
    ax[3].clear()

    ax[0].set_visible(False)
    ax[1].set_visible(False)
    ax[2].set_visible(True)
    ax[3].set_visible(True)

    #ax[0].set_position([0.125, 0.575, 0.85, 0.4])
    #ax[1].set_position([0.125, 0.15, 0.85, 0.4])
    ax[2].set_position([0.125, 0.375, 0.85, 0.6])
    ax[3].set_position([0.125, 0.15, 0.85, 0.2])

    #   F - UPDATE MOUSTURE PLOT
    hy_min = min(valMneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1
    hy_max = max(valMneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1

    ax[2].set_ylim([ hy_min, hy_max ])
    ax[2].set_ylabel("Moisture [%]")

    ax[2].grid(True)   

    # SET X TICK TIME LABEL
    if BUFF_FILL > 1:
        ax[2].set_xticks(my_tick_list)
        ax[2].set_xticklabels(my_clear_list)

    #   F - UPDATE PUMP
    hy_min = min(valPneat[1 , BUFF_LEN-BUFF_FILL:BUFF_LEN]) - 1
    hy_max = max(valPneat[1, BUFF_LEN-BUFF_FILL : BUFF_LEN]) + 1
    
    ax[3].set_ylim([ hy_min, hy_max ])
    ax[3].set_ylabel("PUMP")

    ax[3].grid(True)

    # SET X TICK TIME LABEL
    if BUFF_FILL > 1:
        ax[3].set_xticks(my_tick_list)
        ax[3].set_xticklabels(my_label_list, rotation =45)

    #ax[3].set_xlabel("time [min]")
    f.set_tight_layout(True)

    ax[2].plot( valMneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valMneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )
    ax[3].plot( valPneat[ 0 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] , valPneat[ 1 , BUFF_LEN-BUFF_FILL : BUFF_LEN ] )

def animate(i):
# PLOT VALUES
    global BUFF_FILL, FIRST_SCAN, PLOT_WINDOW

    if not FIRST_SCAN and BUFF_FILL>0:
    # UPDATE PLOTS
        if DEBUG_MODE:
            print(" ")
            print("+- ~ - ~ - ~ - ~ - ~ -+")
            print("   A N I M A T E   ")
            start_plot = time.time()
            start = time.time()

        update_plot()   

        # PRINT PLOTTING TIME
        if DEBUG_MODE:
            end = time.time()
            print("plot time: " + str(end-start))
            print("PLOT WINDOW: " + str(PLOT_WINDOW))
            print("BUFF_FILL: " + str(BUFF_FILL))
                
        if DEBUG_MODE:
            end_plot = time.time()
            print(" ")
            print("ANIMATE time: " + str(end_plot-start_plot))

    if FIRST_SCAN:
        FIRST_SCAN = False

def init_log():
    global LOG_NAME

    if os.path.isfile(LOG_NAME):
    # FILE EXISTS
        if ( time.time() ) - ( os.path.getmtime(LOG_NAME) ) > 600:
        # CHECK IF LOG HAS EXPIRED
            os.remove(LOG_NAME)
            file = open(LOG_NAME, 'w')
            file.close()

        else:
        # LOAD DATA
            my_data_frame = pd.read_csv(LOG_NAME)
            my_data = my_data_frame.values.to_list()

    else:
    # CREATE FILE
        file = open(LOG_NAME, 'w')
        file.close()


def log_data(my_data):
    global FIRST_SCAN, LOG_NAME
    my_data_frame = pd.DataFrame()

    # APPEND TO FILE
    my_data_frame.append(my_data[0,1])

## START PROGRAM / GUI


# SET Y LIMITS
ax[0].set_ylim([10,40])
ax[1].set_ylim([0,255])
ax[2].set_ylim([0,100])
ax[3].set_ylim([0,100])

# SET Y LABEL
ax[0].set_ylabel("TC temp [*C]")
ax[1].set_ylabel("LIGHT")
ax[2].set_ylabel("Moisture [%]")
ax[3].set_ylabel("PUMP")

# SETT GRID
ax[0].grid(True)
ax[1].grid(True)
ax[2].grid(True)
ax[3].grid(True)

#ax[3].set_xlabel("time [min]")

ax[0].plot([0,1], [10,40])
ax[1].plot([0,1], [0,255])
ax[2].plot([0,1], [0,100])
ax[3].plot([0,1], [0,100])

# DEFINE TK STUFF
root = Tk() #init Tk
root.title ("G R O W  .  M A S T E R")
app = App(master=root)  # assign tk to master frame

# ACTIONS WHEN CLOSING WINDOW
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        app.arduino.closeConnection()
        sys.exit()
root.protocol("WM_DELETE_WINDOW", on_closing) # LINK FUNCTION TO CLOSING TRIGGER

cycle_counter = 0
plot_index_prev = 0
plot_index = 0

exportData  = pd.DataFrame()

# PROGRAM TO CALL EVERY .. 
def program():
    global BUFF_FILL, FIRST_SCAN, PLOT_WINDOW
    global valM, valH, valH1, valP, valL
    global valMneat,valHneat, valH1neat, valPneat, valLneat
    global cycle_counter, plot_index, plot_index_prev
    global app

    my_time_list = get_time_list()

    if DEBUG_MODE:
        print(" ")
        print("+-~~~-~~~-~~~-~~~-~~~-~~~-~~~-~~~-~~~-~~~-+")
        print(" ")
        print("   P R O G R A M   ")
        start_prog = time.time()

    # CALL DAYLIGHT SCHEDULER
    app.daylight_sequence()
    app.update_serial()

#   UPDATE ARDUINO STATUS
    if app.arduino.getStatus():
        app.serial_connection_string.set("Connected")

    else:
        app.serial_connection_string.set("Disconnected")

#   GET NEW SAMPLES
    my_tick_list = []
    my_label_list = []
    my_clear_list = []

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
            print("- Shift buffers: " + str(end-start) )
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
            print("- Get values: " + str(end-start) )

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
        my_time_list.insert(0, app.str_time.get())
        if BUFF_FILL>1:
            if BUFF_FILL>6:
                my_label_list = []
                my_tick_list = []
                stepsize = BUFF_FILL/6.0

                for n in range(6):
                    my_label_list.append(my_time_list[int(n*stepsize)])
                    my_tick_list.append(valP[0,int(n*stepsize)])
                    my_clear_list.append("")
                my_label_list.append(my_time_list[BUFF_FILL-1])
                my_tick_list.append(valP[0,BUFF_FILL-1])
                my_clear_list.append("")

            else:
                my_label_list = []
                my_tick_list = []
                my_clear_list = []
                for n in range(BUFF_FILL-1):
                    my_label_list.append(time_list[int(n)])
                    my_tick_list.append(valP[0,n])
                    my_clear_list.append("")
                my_label_list.append(time_list[BUFF_FILL-1])
                my_tick_list.append(valP[0,BUFF_FILL-1])
                my_clear_list.append("")

            set_tick_list(my_tick_list)
            set_time_list(my_time_list)
            set_label_list(my_label_list)
            set_clear_list(my_clear_list)

#   UPDATE PLOT ON TAB CHANGE

    PLOT_WINDOW = app.get_plot()
    if PLOT_WINDOW != plot_index_prev:
        print(" - TAB CHANGED - ")
        update_plot()
    plot_index_prev = PLOT_WINDOW

    # log_data('logging', valM)

    if DEBUG_MODE:
        end_prog = time.time()
        print(" ")
        print("PROGRAM() time: " + str(end_prog-start_prog))

#   UPDATE CYCLE COUNTER AND SCHEDULE NEW PROGRAM CYCLE
    cycle_counter = cycle_counter + 1
    FIRST_SCAN = False
    root.after(int(PROGRAM_CYLCETIME), program)
root.after(int(PROGRAM_CYLCETIME), program)

# START GUI
ani = animation.FuncAnimation(f, animate, interval = int(ANI_CYCLETIME))
app.mainloop()