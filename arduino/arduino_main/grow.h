#ifndef GROW_H
#define GROW_H

#include <Arduino.h>
#include "sensors.h" 
#include "actuators.h"
#include "devices.h"

const int NR_TC = 2;
const int NR_RELAY = 2;

AnalogSensor  moisture;       // MOISTURE SENSOR ANALOG SENSOR
DigitalOutput moisturePower;  // ENABLE POWER TO MOISTURE SENSOR
DigitalInput vlotter;         // FLOAT SWITCH FOR PUMP INTERLOCKING
AnalogSensor thermocouple[NR_TC];    // THERMOCOUPLE ANALOG SENSOR (VOLTAGE READOUT)
DigitalOutput relayboard[NR_RELAY];  // DIGITAL INPUT FOR RELAY BOARD (5V -> OPTOCOUPLER -> RELAY)
RGBWLed lamp;                 // RGBW PWM LIGHT OUTPUT
MotorDriver pump;             // PUMP H-BRIDGE MOTOR DRIVER


#endif
