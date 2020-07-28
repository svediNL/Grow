#ifndef ACTUATORS_H
#include "actuators.h"

void DigitalOutput::set(bool output){
  if(invertOutput){ digitalWrite(pin, !output); }
  else { digitalWrite(pin, output); }
  
  state= output;
}

void DigitalOutput::init(int input, String devName){
  pin = input;
  deviceName = devName;
  pinMode(pin, OUTPUT);
  state = false;
  if(invertOutput){ digitalWrite(pin, state); }
  else { digitalWrite(pin, state); }
}

void DigitalOutput::help(){
  
  Serial.print("  ");
  Serial.print(deviceName);
  Serial.print("\n\r");
  Serial.print("    - Output on pin: ");
  Serial.print(pin);
  Serial.print("\n\r");
}

void RGBWLed::init(String devName, int pinR = -1, int pinG= -1, int pinB= -1, int pinW= -1){
  pinRGBW[0] = pinR;
  pinRGBW[1] = pinG;
  pinRGBW[2] = pinB;
  pinRGBW[3] = pinW;
  deviceName = devName;

  
  for(int n=0;n<4; n++){
    if(pinRGBW[n] != -1){ pinMode(pinRGBW[n], OUTPUT); };
  }
}
void RGBWLed::help(){

  Serial.print("  ");
  Serial.print(deviceName);
  Serial.print("\n\r");

  for(int n=0;n<4; n++){
    Serial.print("   - ");
    Serial.print(cRGBW[n]);
    Serial.print(" output on pin: ");
    Serial.print(pinRGBW[n]);
    Serial.print("\n\r");
  }
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

int RGBWLed::getStatus(){
  if(outputEnabled){ return valRGBW[3]; }
  else { return 0; }
}

void MotorDriver::init(byte dir, byte power, String devName= ""){
  
  deviceName = devName;
  hBridge.pinDir = dir;
  hBridge.pinPWM = power;

  pinMode(hBridge.pinDir, OUTPUT);

  pinMode(hBridge.pinPWM, OUTPUT);

}
void MotorDriver::help(){
  Serial.print("  ");
  Serial.print(deviceName);
  Serial.print("\n\r");
  
  Serial.print("   - Motor direction on pin: ");
  Serial.print(hBridge.pinDir);
  Serial.print("\n\r");
  Serial.print("   - Motor PWM on pin: ");
  Serial.print(hBridge.pinPWM);
  Serial.print("\n\r");
}

void MotorDriver::enableOutput(bool output)
// ENABLE/DISABLE MOTOR PWM OUTPUT
{
  outputEnabled = output;

  if(output && !interlocked)
  // OUTPUT = true  &  NOT INTERLOCKED
  { analogWrite(hBridge.pinPWM, hBridge.outputPWM);}
  else
  // DISABLE BY DEFAULT
  { analogWrite(hBridge.pinPWM, 0); }
}

void MotorDriver::setPWM(int setpoint)
// SET MOTOR PWM OUTPUT
{
  hBridge.outputPWM = setpoint;

  if(outputEnabled && !interlocked)
  // OUTPUT = true  &  NOT INTERLOCKED
  { analogWrite(hBridge.pinPWM, hBridge.outputPWM); }
}

void MotorDriver::setDir(bool bDir)
// SET MOTOR H-BRIDGE DIRECTION PIN
{
  hBridge.outputDir = bDir;
  digitalWrite(hBridge.pinDir, hBridge.outputDir);
}

void MotorDriver::interlock(bool state)
// SET INTERLOCK & ACT ON INTERLOCK
{
  interlocked = state;

  bool tmp;                       // INTERLOCKED OUTPUT STATE 
  tmp = !state && outputEnabled;  // true WHEN NOT INTERLOCKED & ENABLED
  
  if(!tmp)
  // NO OUTPUT TO SET OR OUTPUT INTERLOCKED
  { analogWrite(hBridge.pinPWM, 0); }
  else 
  // ENABLED OUTPUT IS NOT INTERLOCKED
  { enableOutput(true);};
}

int MotorDriver::getStatus()
// GET DRIVE OUTPUT STATUS
{
  int tmp; 
  if(outputEnabled && !interlocked){
    if(hBridge.outputDir){ tmp = -1* hBridge.outputPWM ;}
    else {tmp = hBridge.outputPWM;}
  }
  else{ tmp = 0;}

  return tmp;
}
void MotorDriver::refresh();

#endif
