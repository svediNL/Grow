#ifndef SENSORS_H
#include "sensors.h"

void AnalogSensor::init(int inputpin, String devName, int fsv=1023, float mfsv=3.14, String unit= '[-]'){
  pin = inputpin;
  rawFullScaleValue=fsv;
  metricFullScaleValue=mfsv;
  metric= unit;
  deviceName = devName;
  /*
  Serial.print("Intializing: ");
  Serial.print(deviceName);
  Serial.print("\n\r");

  Serial.print("   Input pin: ");
  if (pin >= 54){   Serial.print(sAnalogPin[pin-54]); }
  else if (pin >= 14){  Serial.print(sAnalogPin[pin-14]);}
  else { Serial.print(pin); }; 

  Serial.print("\n\r");
    
  Serial.print("   Raw Full Scale Value: ");
  Serial.print(rawFullScaleValue);
  Serial.print("\n\r");
  
  Serial.print("   Metric Full Scale Value: ");
  Serial.print(metricFullScaleValue);
  Serial.print(" ");
  Serial.print(metric);
  Serial.print("\n\r");

  Serial.println("");*/
}
    
void AnalogSensor::refresh(){
  rawValue = analogRead(pin);
  metricValue = (float(rawValue) / float(rawFullScaleValue) ) * metricFullScaleValue;
  percentage = (float(rawValue) / float(rawFullScaleValue) ) * 100;
};

int AnalogSensor::getRawValue(){ return rawValue; };

float AnalogSensor::getMetricValue(){ return metricValue; };

void DigitalInput::init(int input, String devName){
  pin =input;
  deviceName = devName;

  pinMode(pin, INPUT_PULLUP);
  pinstate = digitalRead(pin);
/*
  Serial.print("Initalizing: ");
  Serial.print(deviceName);
  Serial.print("\n\r");
  delay(500);
  
  Serial.print("   Input on pin: ");
  Serial.print(pin);
  Serial.print("\n\r");
  
  Serial.println("");*/
};

bool DigitalInput::state(){
  pinstate = digitalRead(pin);
  
  return pinstate;
};

#endif
