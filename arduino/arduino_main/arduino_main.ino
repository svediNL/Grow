#include "comms.h"
#include "sensors.h" 
#include "actuators.h"
#include "grow.h" 

int rawMoisture = 0;

Comms serialMsg;
int counter = 0;
bool bNewMessage = false;

String serialString;
float rntc, vin, vm, rc;
float Tn, Rn, coeffB, temp;

unsigned long runtime;
void setup(){
  // SET THERMOCOUPLE CALCULATION PARAMETERS
  vin = 5.0;    // INPUT VOLTAGE
  rc = 14700;   // BIAS RESISTOR
  Rn = 10000;   // THERMOCOUPLE RESITANCE AT Tn
  Tn = 25;      // THERMOCOUPLE TEMPERATURE AT Rn
  coeffB=3435;  // THERMOCOUPLE COEFFICIENT

  // INIT SERIAL
  Serial.begin(115200);

  // INIT GROW.H DEVICES
  lamp.init("RGBW LED PWM output",11,10,9,8);                       // SETUP LAMP - RGBWLed ON PINS 11,10,9,8
  pump.init(7,6,"pump on H-Bridge board");                          // SETUP PUMP - MotoDriver DIR=7, PWM=6
  moisture.init(A0, "water sensor - analog input", 1023, 100, "%"); // SETUP MOISTURE - AnalogSensor on pin=A0, maxRawInput=1023, maxUserVal= 100%
  thermocouple[0].init(A1, "thermocouple", 1023, 5, "V");              // SETUP THERMOCOUPLE VOLTAGEAnalogSensor on pin=A1, maxRawInput=1023, maxUserVal= 5V
  thermocouple[1].init(A2, "thermocouple", 1023, 5, "V");              // SETUP THERMOCOUPLE VOLTAGEAnalogSensor on pin=A1, maxRawInput=1023, maxUserVal= 5V
  moisturePower.init(22, "water sensor - power enable");            // SETUP DigitalOutput on pin=22
  relayboard[0].init(24, "lighting fan");                           // SETUP DigitalOutput on pin=24
  relayboard[1].init(26, "relay1");                                 // SETUP DigitalOutput on pin=26
  vlotter.init(23, "vlotter");                                      // SETUP DigitalInput on pin=23
}

void loop(){
  runtime = millis();

  if(vlotter.state()) { pump.interlock(true);}
  else { pump.interlock(false); };

  if(bNewMessage){
    serialMsg.message_handler(serialString); // decode serial string
    doCommand();
    bNewMessage = false; 
  }  
}
 
void serialEvent(){
  serialString = Serial.readStringUntil('\n');
  bNewMessage = true;
}

void doCommand(){
  String tmpString;
  char tmpChar;
  int tmpInt;
  bool tmpBool;
  switch(serialMsg.message.inputCommand){

    case GET_MOISTURE:
      delay(2);
      moisturePower.set(true); // enable power
      delay(10);  // let the power settle
      moisture.refresh(); // get value
      moisturePower.set( false);  // disable power

      Serial.print(moisture.getMetricValue()); //print raw value
      Serial.print('@'); // close line
      
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      break;

    case GET_TEMP:
      delay(2);
      tmpInt = serialMsg.message.sParameter[0].toInt();
      thermocouple[tmpInt].refresh();
      vm = thermocouple[tmpInt].getMetricValue();
      if (vin-vm != 0) {
        rntc = (vm*rc)/(vin-vm);
      
        temp = rntc / Rn;
        temp = log(temp);
        temp /= coeffB;
        temp += 1 / (Tn +273.15);
        temp = 1/ temp;
        temp -= 273.15;
        
        Serial.print(temp);
      }
      else { 
        Serial.print(420);
        };
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;
      
    case SET_RELAY:
      delay(2);
      tmpInt = serialMsg.message.sParameter[0].toInt();
      Serial.println(tmpInt);
      if(serialMsg.message.sParameter[1] == "0"){ relayboard[tmpInt].set(false);}
      else if (serialMsg.message.sParameter[1] == "1"){ relayboard[tmpInt].set(true);};
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;
      
    case ENABLE_LAMP:
      delay(2);
      tmpBool = bool(serialMsg.message.sParameter[0].toInt()); 
      
      lamp.enableOutput(tmpBool);
      if(lamp.getStatus()>0)  { relayboard[0].set(true); }
      else                    { relayboard[0].set(false); };
      
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;
      
    case SET_LAMP:
      delay(2);
      tmpString = serialMsg.message.sParameter[0];
      tmpInt = serialMsg.message.sParameter[1].toInt();

      // cycle through RGBW string
      for(int i=0; i<=tmpString.length()-1; i++){
        tmpChar = tmpString[i];
        
        if(tmpChar == 'R'){ lamp.set(R, tmpInt);}
        else if(tmpChar == 'G'){ lamp.set(G, tmpInt);}
        else if(tmpChar == 'B'){ lamp.set(B, tmpInt);}
        else if(tmpChar == 'W'){ lamp.set(W, tmpInt);}

      }

      if(lamp.getStatus()>0)  { relayboard[0].set(true); }
      else                    { relayboard[0].set(false); };
      
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;

    case GET_LAMP:
      delay(2);
      Serial.print(lamp.getStatus());
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;
        
    case ENABLE_PUMP:
      delay(2);
      tmpBool = bool(serialMsg.message.sParameter[0].toInt()); 
      pump.enableOutput(tmpBool);
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;
      
    case SET_PUMP:
      tmpInt = serialMsg.message.sParameter[0].toInt();
      tmpBool = bool(serialMsg.message.sParameter[1].toInt());
      
      pump.setPWM(byte(tmpInt));
      pump.enableOutput(tmpBool);
      
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;

    case GET_PUMP:
      delay(2);
      tmpInt = pump.getStatus();
      Serial.print(tmpInt);
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;
    
    case HELP:
      delay(2);
      printHelp();
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;
       
    case NO_COMMAND:
      delay(2);
      Serial.println("DEV_COMM_ERR");
      Serial.print('@');
      break;
  }
  
}

void printHelp(){
  Serial.println("====================================================");
  Serial.println("    + + + + + +     ARDUINO GROW     + + + + + +    ");
  Serial.println("====================================================");
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("- Commands use the following syntax: ");
  Serial.println("  COMMAND(PAR1, PAR2, PAR3, ETC)\n");
  Serial.println("");
  Serial.println("List of commands:");
  Serial.println("   ENABLE_LAMP( enable[0/1] )");
  Serial.println("   ENABLE_PUMP( enable[0/1] )"); 
  Serial.println("   SET_LAMP   ( colour[R,B,G,W],  value[0-255], enable[0/1] )");
  Serial.println("   SET_PUMP   ( value[0-255],   enable[0/1] )"); 
  Serial.println("   SET_RELAY  ( index[0-1],   value[0/1] )");
  Serial.println("   GET_MOISTURE( )");
  Serial.println("   GET_TEMP( index[0-1] )");
  Serial.println("   GET_LAMP( )");
  Serial.println("   GET_PUMP( )"); 
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("DEVICE CONNECTIONS");
  Serial.println("");
  moisture.help();
  Serial.println("");
  moisturePower.help();
  Serial.println("");
  vlotter.help();
  Serial.println("");
  thermocouple[0].help();
  Serial.println("");
  thermocouple[1].help();
  Serial.println("");
  relayboard[0].help(); 
  Serial.println("");
  relayboard[1].help(); 
  Serial.println("");
  lamp.help();
  Serial.println("");
  pump.help();
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("====================================================");
  Serial.print('@');
}
