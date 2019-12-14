#ifndef ACTUATORS_H
#include "actuators.h"

void DigitalOutput::set(bool output){
  digitalWrite(pin, output);
  state= output;
}

void DigitalOutput::init(int input, String devName){
  pin = input;
  deviceName = devName;
  pinMode(pin, OUTPUT);
  digitalWrite(pin, false);
  /*
  Serial.print("Initalizing: ");
  Serial.print(deviceName);
  Serial.print("\n\r");
  delay(500);
  
  Serial.print("   Output on pin: ");
  Serial.print(pin);
  Serial.print("\n\r");
  
  Serial.println("");
  */
}

void RGBWLed::init(String devName, int pinR = -1, int pinG= -1, int pinB= -1, int pinW= -1){
  pinRGBW[0] = pinR;
  pinRGBW[1] = pinG;
  pinRGBW[2] = pinB;
  pinRGBW[3] = pinW;
  deviceName = devName;
  /*
  Serial.print("Initalizing: ");
  Serial.print(deviceName);
  Serial.print("\n\r");
  delay(500);
  */
  
  for(int n=0;n<4; n++){
    if(pinRGBW[n] != -1){ pinMode(pinRGBW[n], OUTPUT); };

    /*
    Serial.print("   ");
    Serial.print(cRGBW[n]);
    Serial.print(" output on pin: ");
    Serial.print(pinRGBW[n]);
    Serial.print("\n\r");
    delay(200);
    */
  }
  //Serial.println("");
}

void RGBWLed::set(RGBWenum colour, int value){
  valRGBW[colour] = value;
  if(outputEnabled) { analogWrite(pinRGBW[colour], valRGBW[colour]); }
}

void RGBWLed::enableOutput(bool output){
  outputEnabled = output;

  if(outputEnabled){
    for(int n=0; n<4; n++){
       analogWrite(pinRGBW[n], valRGBW[n]);
    }
  }
  else {
    for(int n=0; n<4; n++){
       analogWrite(pinRGBW[n], 0);
    }
  }
}

void MotorDriver::init(byte dir, byte power, String devName= ""){
  
  deviceName = devName;
  hBridge.pinDir = dir;
  hBridge.pinPWM = power;
  /*
  Serial.print("Initalizing: ");
  Serial.print(deviceName);
  Serial.print("\n\r");
  delay(200);
  
  Serial.print("   Motor direction on pin: ");
  Serial.print(hBridge.pinDir);
  Serial.print("\n\r");
  */
  pinMode(hBridge.pinDir, OUTPUT);
  /*
  delay(200);
  
  Serial.print("   Motor PWM on pin: ");
  Serial.print(hBridge.pinPWM);
  Serial.print("\n\r");
  */
  pinMode(hBridge.pinPWM, OUTPUT);
  
  
  //Serial.println("");
}

void MotorDriver::enableOutput(bool output){
  if(output){
    analogWrite(hBridge.pinPWM, hBridge.outputPWM);
  }
  else{
    analogWrite(hBridge.pinPWM, 0);
  }

  outputEnabled = output;
}

void MotorDriver::setPWM(int setpoint){
  hBridge.outputPWM = setpoint;
  if(outputEnabled){ analogWrite(hBridge.pinPWM, hBridge.outputPWM); }
}

void MotorDriver::setDir(bool bDir){
  hBridge.outputDir = bDir;
  digitalWrite(hBridge.pinDir, hBridge.outputDir);
}

void MotorDriver::interlock(bool state){
  bool tmp;
  tmp = !state && outputEnabled;
  
  if(!tmp){ analogWrite(hBridge.pinPWM, 0); }
  else { enableOutput(true);};


  interlocked = state;
}

#endif
