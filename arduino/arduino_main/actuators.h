#ifndef ACTUATORS_H
#define ACTUATORS_H

#include <Arduino.h>
#include "timekeeping.h"

enum RGBWenum {R, G, B , W};

class DigitalOutput{
  public:
    int pin;
    String deviceName;
    bool state;
    bool invertOutput = false;
    
    void init(int input, String devName);
    void help();
    void set(bool output);
    
};

class RGBWLed {
  public:
    int pinRGBW[4];
    int valRGBW[4];
    String deviceName;
    
    void init(String devName, int pinR = -1, int pinG= -1, int pinB= -1, int pinW= -1);
    void help();
    void set(RGBWenum colour, int value);
    int getStatus();
    void enableOutput(bool output);


  private:
    RGBWenum eRGBW;
    bool outputEnabled;
    char cRGBW[4] = {'R','G','B','W'};
};


//class IncEncoder{
  
//}

class HBridge {
  public:

    bool outputDir = false;
    byte pinDir;
    
    byte outputPWM = 0;
    byte pinPWM;
     
    
    private:
      
};

class MotorDriver{
  public:
    String deviceName;
    
    void init(byte dir, byte power, String devName= "");
    
    void refresh(TimeKeeper myClock);
    
    void enableOutput(bool output);
    
    void setPWM(int setpoint);
    void setDir(bool dir);
    void set_schedule(int parTime, int setpoint); // setpoint can be positive or negative
    
    void interlock(bool state);
    int getStatus();
    
    void help();
  
  private:
    bool outputEnabled;
    bool interlocked;
    HBridge hBridge; 
    
};


#endif
