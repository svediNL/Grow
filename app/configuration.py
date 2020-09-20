### USE THIS DOCUMENT TO CONFIGURE WHAT DEVICES YOU WANT TO ADD TO YOUR SETUP
## GUI WILL AUTO GENERATE BASED ON DEVICES LISTED HERE
DEBUG_MODE = True

## D E V I C E   D E F I N I T I O N
# ARDUINO
SERIAL_PORT = ""	# DEFAULT SERIAL PORT TO USE AT INIT (CAN BE EMPTY STRING IF UNKOWN)
BAUD_RATE   = 115200			# STANDARD BAUD RATE USED AT INIT


# THERMOCOUPLES
NAMES_THERMO 	= ["TC_A", "TC_B"]		# DISPLAY NAMES OF THERMOCOUPLES ->	example: NAMES_THERMO = ["ground temperature", "air temperature"]
UNIT_THERMO	= "[deg. C]"			# MEASURED UNITS OF THERMOCOUPLE
NR_THERMO 		= len(NAMES_THERMO)		# NR OF THERMOCOUPLES	(CALCULATED)

# LED DRIVER (PWM)					
NAMES_LAMP 		= [ "LED_A" ]		# DISPLAY NAME OF LAMP UNITS ->	example: NAMES_LAMP = ["my RGBW Lamp", "my Simple Lamp"]													
CHANNELS_LAMP	= [ ['R','G','B','W'] ]			# RGBW CHANNELS FOR EACH LAMP MODULE ->	2D-array [lamp, channel] ->	example: CHANNELS_LAMP = [ ['R','G','B','W'] , ['W'] ]		
UNIT_LAMP	= "[-]"								# MEASURED UNITS OF LAMP			
NR_LAMP 		= len(NAMES_LAMP)	# NR OF CONTROLABLE LAMPS	(CALCULATED)

# MOISTURE SENSORS
NAMES_MOISTURE 	= ["MOISTURE_A"]		# DISPLAY NAMES OF ANALOG RESISTIVE MOISTURE SENSORS ->	example: NAMES_MOISTURE = ["moisture small pot", "moisture big pot"]
UNIT_MOISTURE	= "[%]"								# MEASURED UNITS OF MOISTURE SENSOR
NR_MOISTURE 	= len(NAMES_MOISTURE)	# NR OF ANALOG RESISTIVE MOISTURE SENSORS (CALCULATED)


# H-BRIDGE BASED PUMP (PWM, DIRECTION)
NAMES_PUMP	= ["PUMP_A"]			# PUMP DISPLAY NAMES -> ONLY ONE IS SUPPORTED ATM
UNIT_PUMP	= "[-]"								# MEASURED UNITS OF PUMP
NR_PUMP 	= len(NAMES_PUMP)	# NUMBER OF PUMPS	(CALCULATED)

# RELAYS (FANS, VALVES, PUMPS, LIGHTS)
# NAMES_RELAY	= [""," Q IN (0)", "Q WASTE (2)", "Q WATER (3)", "Q NUTR (4)", "Q OUT (5)", "FANS LAMP", "NC"]		# DISPLAY NAMES OF RELAYBOARD CHANNELS
NAMES_RELAY	= ["12V Enable"," Q IN (0)", "Q WASTE (2)", "Q WATER (3)", "Q NUTR (4)", "Q OUT (5)", "FANS LAMP", "NC"]		# DISPLAY NAMES OF RELAYS
UNIT_RELAY	= "[0/1]"
NR_RELAY 	= len(NAMES_RELAY)																								# NR OF RELAYS (CALCULATED)

# VALVE CIRCUITS
NAMES_FLOW 		= ["WATER-INPUT", "NUTR.-INPUT", "OUTPUT-WASTE", "OUTPUT-INPUT"]		# DISPLAY NAMES OF FLOW CIRCUITS
VALVES_FLOW 	= [ [1,3], [1,4], [2,5], [1,5] ]										# LIST OF VALVE INDICES TO OPEN PER FLOW CIRCUIT [CIRUIT][VALVES]
FORCE_INTERLOCK = [True, True, False, False, True]										# FORCE PUMP INTERLOCK WHEN CERTAIN FLOW INDEX IS SELECTED, LAST INDEX IS FOR WHEN FLOW CIRCOUT IS DISABLED
NR_FLOW 		= len(NAMES_FLOW)														# NR OF FLOW CIRCUITS (CALCULATED)


## T I M I N G   D E F I N I T I O N
PROGRAM_CYLCETIME	= 500.0		#	CALL PROGRAM FUNCTION EVERY .. ms
SAMPLE_RATE 		= 1				#	GET A SAMPLE EVERY .. PROGRAM CYCLES
BUFF_LEN 			= 4096			#	SAMPLE BUFFER LENGTH
PLOT_REFRESH_RATE	= 1	
ANI_CYCLETIME 		= 10000.0		#	UPDATE PLOT / CALL ANIMATION FUNCTION EVERY .. ms

## P L O T T I N G   D E F I N I T I O N
ENABLE_DYNAMIC_RANGE_THERMO		= True
ENABLE_DYNAMIC_RANGE_LAMP		= False
ENABLE_DYNAMIC_RANGE_MOISTURE	= False
ENABLE_DYNAMIC_RANGE_PUMP		= True

DEFAULT_RANGE_THERMO 	= [10, 35]
DEFAULT_RANGE_LAMP		= [0, 255]
DEFAULT_RANGE_MOISTURE 	= [0, 100]
DEFAULT_RANGE_PUMP		= [0, 255]

PLOT_NAMES = ["OVERVIEW", "LIGHT", "MOISTURE"]
NR_PLOT = len(PLOT_NAMES)

LOG_NAME	= 'myLog.csv'

## G U I   D E S I G N
BG_MAIN			= "gray30"	#"gray93"
BG_SUB 			= "gray33"	#"gray96"
BG_SUBSUB 		= "white"	#"white"
BG_TOG_A		= "gray44"	#"gray96"
BG_TOG_B 		= "gray30"	#"gray93"
BG_TAB 			= "gray44"	#"gray85"
BG_TAB_ACTIVE 	= "gray33"	#"gray96"
BG_ENTRY		= "gray60"	#"white"
BG_BUTTON		= "black"
BG_CHECK		= "gray40"

FG_TEXT			= "white"	#"black"
FG_ENTRY		= "white"


