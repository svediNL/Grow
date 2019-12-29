#ifndef COMMS_H
#define COMMS_H

#include <Arduino.h>

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
