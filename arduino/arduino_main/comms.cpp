#ifndef COMMS_H
#include "comms.h"
#include "sensors.h" 
#include "actuators.h"

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
    else if (message.sCommand == "ENABLE_PUMP"){ message.inputCommand = ENABLE_PUMP; } 
    else if (message.sCommand == "SET_PUMP"){ message.inputCommand = SET_PUMP; }
    else if (message.sCommand == "MOT_PWM"){ message.inputCommand = SET_MOTOR_PWM; }
    else if (message.sCommand == "MOT_DIR"){ message.inputCommand = SET_MOTOR_DIR; }
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

void Comms::printHelp(){
  Serial.println("====================================================");
  Serial.println("    + + + + + +     ARDUINO GROW     + + + + + +    ");
  Serial.println("====================================================");
  Serial.println("");
  Serial.println("- Commands use the following syntax: ");
  Serial.println("  COMMAND(PAR1, PAR2, PAR3, ETC)\n");
  Serial.println("");
  Serial.println("List of commands:");
  Serial.println("   GET_MOISTURE( )");
  Serial.println("   GET_TEMP( )");
  Serial.println("   SET_RELAY( index[0-1], value[0/1] )");
  Serial.println("   SET_LAMP( R/B/G/W, value[0-255], enable[0/1] )");
  Serial.println("   SET_PUMP( value[0-255] , enable[0/1] )");
  Serial.println("   ENABLE_LAMP( enable[0/1] )");
  Serial.println("   ENABLE_PUMP( enable[0/1] )");  
  Serial.println("====================================================");
}

#endif
