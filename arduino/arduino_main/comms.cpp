#ifndef COMMS_H
#include "comms.h"


void Comms::message_handler(String inputString){
  
    seperateString(inputString);
    message.sCommand.toUpperCase();
    for(int n=0; n<6; n++){ message.sParameter[n].toUpperCase();};

    //printMessage();
    
    if      (message.sCommand == "GET_MOISTURE"){ message.inputCommand = GET_MOISTURE; }
    else if (message.sCommand == "GET_TEMP"){ message.inputCommand = GET_TEMP; }
    else if (message.sCommand == "SET_RELAY"){ message.inputCommand = SET_RELAY; }
    else if (message.sCommand == "ENABLE_LAMP"){ message.inputCommand = ENABLE_LAMP; }
    else if (message.sCommand == "SET_LAMP"){ message.inputCommand = SET_LAMP; }
    else if (message.sCommand == "GET_LAMP"){ message.inputCommand = GET_LAMP; }
    else if (message.sCommand == "ENABLE_PUMP"){ message.inputCommand = ENABLE_PUMP; } 
    else if (message.sCommand == "SET_PUMP"){ message.inputCommand = SET_PUMP; }
    else if (message.sCommand == "GET_PUMP"){ message.inputCommand = GET_PUMP; }
    else if (message.sCommand == "SET_TEMP_RC"){ message.inputCommand = SET_TEMP_RC; }
    else if (message.sCommand == "IGNORE_PUMP_INTERLOCK"){ message.inputCommand = IGNORE_PUMP_INTERLOCK; }
    else if (message.sCommand == "SET_CLOCK"){ message.inputCommand = SET_CLOCK; }
    else if (message.sCommand == "GET_CLOCK"){ message.inputCommand = GET_CLOCK; }
    else if (message.sCommand == "GET_EPOCH"){ message.inputCommand = GET_EPOCH; }
    else if (message.sCommand == "TIMER_OUTPUT"){ message.inputCommand = TIMER_OUTPUT; }
    else if (message.sCommand == "TIMER_CLAIMED"){ message.inputCommand = TIMER_CLAIMED; }
    else if (message.sCommand == "CLAIM_TIMER"){ message.inputCommand = CLAIM_TIMER; }
    else if (message.sCommand == "RELEASE_TIMER"){ message.inputCommand = RELEASE_TIMER; }
    else if (message.sCommand == "SET_TIMER"){ message.inputCommand = SET_TIMER; }
    else if (message.sCommand == "RESET_TIMER"){ message.inputCommand = RESET_TIMER; }
    else if (message.sCommand == "STOP_TIMER"){ message.inputCommand = STOP_TIMER; }
    else if (message.sCommand == "H" || message.sCommand == "HELP"){ message.inputCommand = HELP; }
    else {message.inputCommand = -1;};
    //else if (message.sCommand == ""){ message.inputCommand = ; }

    //clear varialable
    message.sInput = "";
    message.sCommand = "";
    //for(int n=0; n < sizeof(sParameter); n++)  { sParameter[n] = "";};
    parIndex = 0;
    cmdBool = true;
    Serial.flush();
}

void Comms::printMessage(int type = 0) {
  switch(type)
  {
    case 0:
      Serial.println(" ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ");
      Serial.println("Input: " + message.sInput);
      Serial.println("Command: " + message.sCommand);
      Serial.println("Parameter[0]: " + message.sParameter[0]);
      Serial.println("Parameter[1]: " + message.sParameter[1]);
      Serial.println("Parameter[2]: " + message.sParameter[2]);
      Serial.println("Parameter[3]: " + message.sParameter[3]);
  }
}

void Comms::receive_message(){

    
}

void Comms::seperateString(String inputString){
  for(int n=0; n<=inputString.length()-1; n++){
    char inputChar = inputString[n]; 
    
    if (inputChar ==  '('){ 
    //
      receiveStage = 1;
      cmdBool = false;
    } 
    else if (inputChar == ','){
      receiveStage = 2;
    }
    else if (n == inputString.length() - 1 || inputChar == ')'){ 
      if( inputChar != ')'){ tmpString += inputChar;}; //only add to string when not properly closed but end of line
      if (!cmdBool){ receiveStage = 2;}
      else{receiveStage =1;};
      
    }
    else if (inputChar == ' ' || inputChar == ')'){
      receiveStage = 99;    
    };

    //Serial.println("___________");
    //Serial.println(cmdBool);
    //Serial.println(receiveStage);

    switch(receiveStage)
    {
      case 0:
        //IDLE
        tmpString += inputChar; 
        break;
      case 1:
        //SET COMMAND
        message.sCommand =tmpString;
        tmpString = "";
        receiveStage = 0;
        break;
      case 2:
        //ADD PARAMETER
        message.sParameter[parIndex] = tmpString;
        parIndex++;
        tmpString = "";
        receiveStage = 0;
        break;
      case 99:
        //IGNORE CHAR CASE
        receiveStage= 0;
        break;
        
    };
    }
  
}
#endif
