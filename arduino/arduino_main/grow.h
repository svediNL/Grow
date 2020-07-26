#ifndef GROW_H
#define GROW_H

#include <Arduino.h>
#include "sensors.h" 
#include "actuators.h"
#include "devices.h"
#include "timekeeping.h"

// ENABLE/DISABLE DEVICES

// ON/OFF LEVEL SENSOR (FLOAT SWITCH)
const bool  ENABLE_PUMP_INTERLOCK_SWITCH  		= true;   	// SETUP HAS FLOAT SWITCH
const int   NR_FLOAT_SWITCH               		= 1;		// NUMBER OF FLOAT SWITCHES TO BE CONFIGURED
const int   FLOAT_SWITCH_PIN[NR_FLOAT_SWITCH]	= {23};		// PIN NR OF FLOAT SWITCH(es)
const int   FLOAT_PUMP_INTERLOCK_LINKING[NR_FLOAT_SWITCH]  		= {0};    	// LINK FLOAT SWITCH TO PUMP(s)
//const int   FLOAT_VALVE_INTERLOCK_LINKING  		= {0};    	// LINK FLOAT SWITCH TO VALVE(s)

DigitalInput vlotter[NR_FLOAT_SWITCH];         // INSTANCE OF LOAT SWITCH FOR PUMP INTERLOCKING


// THERMOCOUPLE CONFIGURATION
const int     NR_TC           = 2;                  // NUMBER OF THERMOCOUPLE TO BE CONFIGURED
const int     TC_PIN[NR_TC]   = {A1, A2};           // ARRAY OF ANALOG INPUT PINS
const String  TC_NAME[NR_TC]  = {"thermocouple 0", "thermocouple 1"};

AnalogSensor thermocouple[NR_TC]; // INSTANCE THERMOCOUPLE ANALOG SENSOR (VOLTAGE READOUT)


// RELAY CONFIGURATION
const int NR_RELAY                = 8;                                  // NUMBER OF RELAYS TO BE CONFIGURED
const int RELAY_PIN[NR_RELAY]     = {24, 26, 28, 30, 32, 34, 36, 38};   // ARRAY OF DIGITAL OUTPUT PINS
const String RELAY_NAME[NR_RELAY] = {"12V Enable", "Valve 0", "Valve 2", "Valve 3", "Valve 4", "Valve 5", "Fans Lamp", "NC"};

DigitalOutput relayboard[NR_RELAY];                                 // INSTANCE OF DIGITAL OUTUT FOR RELAY BOARD (5V -> OPTOCOUPLER -> RELAY)


// MOISTURE SENSOR CONFIGURATION
const int     NR_MOISTURE                       = 1;     // number of MOISTURE SENSORs to be configured
const int     MOISTURE_INPUT_PIN [NR_MOISTURE]  = {A0};  // array of ANALOG INPUT PINs
const int     MOISTURE_POWER_PIN [NR_MOISTURE]  = {22};  // array of DIGITAL OUTPUT PINs
const String  MOISTURE_NAME [NR_MOISTURE]       = {"water sensor - analog input"};
const String  MOISTURE_POWER_NAME [NR_MOISTURE] = {"water sensor - power enable"};

AnalogSensor  moisture[NR_MOISTURE];                // INSTANCE OF MOISTURE SENSOR ANALOG SENSOR
DigitalOutput moisturePower[NR_MOISTURE];           // INSTANCE OF POWER ENABLE TO MOISTURE SENSOR


// PUMP H-BRIDGE CONFIGURATION
const int     NR_PUMP                 = 1;    // NUMBER OF PUMPS TO CONFIGURE
const int     PUMP_DIR_PIN [NR_PUMP]  = {7};  // ARRAY OF PWM PINS
const int     PUMP_PWM_PIN [NR_PUMP]  = {6};  // ARRAY OF PWM PINS
const String  PUMP_NAME[NR_PUMP]      = {"pump on H-Bridge board"};

MotorDriver pump[NR_PUMP];             // INSTANCE OF PUMP H-BRIDGE MOTOR DRIVER


// PWM DIMMABLE LAMP CONFIGURATION
const int     NR_LAMP                   = 1;                // NUMBER OF LAMPS TO BE CONFIGURED
const int     LAMP_RGBW_PIN[NR_LAMP][4] = { {11,10,9,8} };  // 2D ARRAY OF PWM PINS
const String  LAMP_NAME[NR_LAMP]        = {"RGBW LED PWM output"};

RGBWLed lamp[NR_LAMP];                                // INSTANCE OF RGBW PWM LIGHT OUTPUT

// CONFIGURE DOOR SWITCH TO DIM LIGHT WHEN DOOR OPENS
const bool  ENABLE_FRIDGE_DOOR  = true;   // light dims when door opens
const int   DOOR_SWITCH_PIN    = 25;     // DIGITAL OUTPUT PIN          
DigitalInput doorSensor;                              // INSTANCE OF DOOR SENSOR FOR DIMMING OF LIGHT

TimeKeeper masterClock;

#endif
