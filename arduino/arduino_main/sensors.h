#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>

class AnalogSensor{ 
  public:
    String deviceName;
    
    void init(int inputpin, String devName, int fsv=1023, float mfsv=3.14, String unit= '[-]');
    void refresh();
    int getRawValue();
    float getMetricValue();

    private:
      int pin;
      int rawValue;
      float metricValue;
      float percentage;
      int rawFullScaleValue;
      float metricFullScaleValue;
      String metric;
      String sAnalogPin[8] = {"A0","A1","A2","A3","A4","A5","A6","A7"};

    
      
};

class DigitalInput {
  public:
    void init(int input, String devName);
    bool state();
    
  private:
    String deviceName;
    int pin;
    int pinstate;
};



#endif
