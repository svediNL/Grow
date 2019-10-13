#ifndef GROW_H
#define GROW_H

#include <Arduino.h>
#include "sensors.h" 
#include "actuators.h"
#include "devices.h"

AnalogSensor  moisture;     //moisture analog input
DigitalOutput moisturePower; //enable power to moisture sensor

DigitalInput vlotter;

AnalogSensor thermocouple;

DigitalOutput relayboard[2]; //relay IN1 on relay board


RGBWLed lamp;

MotorDriver pump;
#endif
