#ifndef COMMS_H
#define COMMS_H

#include <Arduino.h>
#include "sensors.h" 
#include "actuators.h"

/*
 * 
 * GET_MOISTURE
 * SET_MOISTURE[ID#, BOOL]
 * SET_FLOW[PERCENTAGE]
 * 
 * SET_LIGHT[ID#, BOOL]
 * 
 * 
 * 
*/

enum Command { 
  GET_MOISTURE, GET_TEMP, 
  SET_RELAY, SET_LAMP, SET_PUMP,
  GET_RELAY, GET_LAMP, GET_PUMP,
  ENABLE_LAMP, ENABLE_PUMP, 
  SET_TEMP_RC,
  IGNORE_PUMP_INTERLOCK,
  SET_CLOCK, GET_CLOCK, GET_EPOCH,
  TIMER_OUTPUT, TIMER_CLAIMED, 
  CLAIM_TIMER, RELEASE_TIMER,
  SET_TIMER, RESET_TIMER, STOP_TIMER,
  DEVICE_TIMER,
  HELP, NO_COMMAND
};

struct Message {
    String sInput;
    String sCommand;
    Command inputCommand = NO_COMMAND;
    String sParameter[6];
};

class Comms {

  public:
    Message message;
    
    int parIndex = 0;
    
    void printMessage(int type = 0);
    void receive_message();
    void message_handler(String inputString);

   private:
    int receiveStage=0;
    boolean cmdBool = true;
    String tmpString;
    void seperateString(String inputString);
};



#endif
