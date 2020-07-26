#ifndef GROW_H
#include "grow.h"
void Grow::fridge_door()
{
  ;
};

void Grow::init(){
  // SETUP CLOCK
  masterClock.set_base_time(16000000);
  masterClock.set_base_prescaler(1024);
  masterClock.set_output_compare(243);
  masterClock.set_time("12:00:00");
  masterClock.set_magic_comp(6379);
  masterClock.init();
  
  // SETUP   P U M P
  for(int n=0; n<NR_PUMP; n++){ 
    overrule_pump_interlock[n] = false; 
    pump[n].init(PUMP_DIR_PIN[n], PUMP_PWM_PIN[n], PUMP_NAME[n]); // SETUP PUMP
  }
  
  if(ENABLE_PUMP_INTERLOCK_SWITCH && NR_FLOAT_SWITCH>0){
    for(int n=0;n<NR_LAMP; n++){ 
      vlotter[n].init(FLOAT_SWITCH_PIN[n], "float switch");   // SETUP FLOAT SWITCH - DigitalInput on pin=23
    }
  }
  
  // SETUP   T H E R M O C O U P L E
  // SET THERMOCOUPLE CALCULATION PARAMETERS
  vin = 5.0;        // INPUT VOLTAGE                  [V]
  Rn = 10000;       // THERMOCOUPLE RESITANCE AT Tn   [ohm]
  Tn = 25;          // THERMOCOUPLE TEMPERATURE AT Rn [C]
  coeffB=3435;      // THERMOCOUPLE COEFFICIENT       [K] -> B= ln(Rt1/Rt2)/(T1^-1 - T2^-1)
  
  for(int n=0;n<NR_TC; n++){ 
    rc[n] = 14700;    // BIAS RESISTOR                  [ohm]
    thermocouple[n].init(TC_PIN[n], TC_NAME[n], 1023, 5, "V");               // SETUP THERMOCOUPLE VOLTAGE - AnalogSensor maxRawInput=1023, maxUserVal= 5V
  };
  
  // SETUP   L A M P
  for(int n=0;n<NR_LAMP; n++){ 
    lamp[n].init(LAMP_NAME[n],LAMP_RGBW_PIN[n][0],LAMP_RGBW_PIN[n][1],LAMP_RGBW_PIN[n][2],LAMP_RGBW_PIN[n][3]);  // SETUP LAMP - RGBWLed ON PINS 11,10,9,8
  }
  if(ENABLE_FRIDGE_DOOR){
    doorSensor.init(DOOR_SWITCH_PIN, "Door switch");
  }
  // SETUP   M O I S T U R E 
  for(int n=0;n<NR_MOISTURE; n++){ 
    moisture[n].init(MOISTURE_INPUT_PIN[n], MOISTURE_NAME[n] , 1023, 100, "%");    // SETUP MOISTURE              - AnalogSensor on pin=A0, maxRawInput=1023, maxUserVal= 100%
    moisturePower[n].init(MOISTURE_POWER_PIN[n], MOISTURE_POWER_NAME[n] );               // SETUP MOISTURE POWER ENABLE - DigitalOutput on pin=22
  }
  
  // SETUP   R E L A Y
  for(int n=0;n<NR_RELAY; n++){ 
    relayboard[n].init(RELAY_PIN[n], RELAY_NAME[n]);    // SETUP RELAYBOARD INPUT INx
  }
};
#endif
