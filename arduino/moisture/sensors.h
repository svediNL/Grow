#ifndef SENSORS_H
#define SENSORS_H

include "comms.h"
struct AnalogSensor{ 
  int rawValue;
  float metricValue;
  float percentage;
  int rawFullScaleValue=1023;
  float metricFullScaleValue=3.14;
  String metric= '[-]';
  Message hello;
}; 

#endif
