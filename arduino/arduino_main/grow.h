#ifndef GROW_H
#define GROW_H

#include <Arduino.h>
#include "sensors.h" 
#include "actuators.h"
#include "devices.h"

// CHANGE THESE NUMBERS TO INCREASE ARRAY -> DONT FORGET TO DEFINE INPUT IN setup()
const int NR_TC = 2;
const int NR_RELAY = 2;
const int NR_MOISTURE = 2;
const int NR_PUMP = 2;
const int NR_LAMP = 2;


AnalogSensor  moisture[NR_MOISTURE];       // MOISTURE SENSOR ANALOG SENSOR
DigitalOutput moisturePower[NR_MOISTURE];  // ENABLE POWER TO MOISTURE SENSOR

AnalogSensor thermocouple[NR_TC];    // THERMOCOUPLE ANALOG SENSOR (VOLTAGE READOUT)

DigitalOutput relayboard[NR_RELAY];  // DIGITAL INPUT FOR RELAY BOARD (5V -> OPTOCOUPLER -> RELAY)

RGBWLed lamp[NR_LAMP];                 // RGBW PWM LIGHT OUTPUT

MotorDriver pump[NR_PUMP];             // PUMP H-BRIDGE MOTOR DRIVER
DigitalInput vlotter[NR_PUMP];         // FLOAT SWITCH FOR PUMP INTERLOCKING


#endif
