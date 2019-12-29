#include "comms.h"
#include "sensors.h" 
#include "actuators.h"
#include "grow.h" 

int rawMoisture = 0;

Comms serialMsg;
int counter = 0;
bool bNewMessage = false;

String serialString;
float rntc, vin, vm, rc[2];
float Tn, Rn, coeffB, temp;

unsigned long runtime;
void setup(){
  // SET THERMOCOUPLE CALCULATION PARAMETERS
  vin = 5.0;    // INPUT VOLTAGE                  [V]
  rc[0] = 14700;   // BIAS RESISTOR               [ohm]
  rc[1] = 14700;   // BIAS RESISTOR
  Rn = 10000;   // THERMOCOUPLE RESITANCE AT Tn   [ohm]
  Tn = 25;      // THERMOCOUPLE TEMPERATURE AT Rn [C]
  coeffB=3435;  // THERMOCOUPLE COEFFICIENT       [K] -> B= ln(Rt1/Rt2)/(T1^-1 - T2^-1)

  // INIT SERIAL
  Serial.begin(115200);

  // INIT GROW.H DEVICES
  lamp[0].init("RGBW LED PWM output",11,10,9,8);                       // SETUP LAMP - RGBWLed ON PINS 11,10,9,8
  pump[0].init(7,6,"pump on H-Bridge board");                          // SETUP PUMP - MotoDriver DIR=7, PWM=6
  moisture[0].init(A0, "water sensor - analog input", 1023, 100, "%"); // SETUP MOISTURE - AnalogSensor on pin=A0, maxRawInput=1023, maxUserVal= 100%
  thermocouple[0].init(A1, "thermocouple", 1023, 5, "V");              // SETUP THERMOCOUPLE VOLTAGEAnalogSensor on pin=A1, maxRawInput=1023, maxUserVal= 5V
  thermocouple[1].init(A2, "thermocouple", 1023, 5, "V");              // SETUP THERMOCOUPLE VOLTAGEAnalogSensor on pin=A1, maxRawInput=1023, maxUserVal= 5V
  moisturePower[0].init(22, "water sensor - power enable");            // SETUP DigitalOutput on pin=22
  relayboard[0].init(24, "lighting fan");                              // SETUP DigitalOutput on pin=24
  relayboard[1].init(26, "relay1");                                    // SETUP DigitalOutput on pin=26
  vlotter[0].init(23, "vlotter");                                      // SETUP DigitalInput on pin=23
}

void loop(){
  runtime = millis();

  if(vlotter[0].state()) { pump[0].interlock(true);}
  else { pump[0].interlock(false); };

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
  char tmpChar[4];
  int tmpInt[4];
  bool tmpBool[4];
  switch(serialMsg.message.inputCommand){

// PRINT MOISTURE VALUE
    case GET_MOISTURE:
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();  // GET CMD INDEX
      
      // GET VALUE
      moisturePower[tmpInt[0]].set(true);    // enable power
      delay(10);                  // let the power settle
      moisture[tmpInt[0]].refresh();         // get value
      moisturePower[tmpInt[0]].set( false);  // disable power

      // PRINT VALUE
      Serial.print(moisture[tmpInt[0]].getMetricValue()); //print raw value
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// PRINT TEMPERATURE VALUE
    case GET_TEMP:
      // GET TC MEASUREMENT
      delay(2); // DELAY SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();  // GET CMD INDEX
      
      thermocouple[tmpInt[0]].refresh();                    // UPDATE TC VALUE
      vm = thermocouple[tmpInt[0]].getMetricValue();        // TRANSLATE TO MEASURED VOLTAGE
      
      if (vin-vm != 0) { // PREVENT DIVIDE BY ZERO
        rntc = (vm*rc[tmpInt[0]])/(vin-vm);                 //GET RESISTANCE OF THERMOCOUPLE 

        // TRANSFORM RESISTANCE TO TEMPERATURE
        temp = rntc / Rn;                                   // A   =   Rntc/Rn    [-]
        temp = log(temp);                                   // tmp =   ln(Rntc/Rn)    [-]
        temp /= coeffB;                                     // tmp =   ln(Rntc/Rn) / coeff   = Tntc^-1 - Tn^-1   [K]
        temp += 1 / (Tn +273.15);                           // tmp = Tntc^-1  [K]
        temp = 1/ temp;                                     // tmp = Tntc   [K]
        temp -= 273.15;                                     // tmp = Tntc   [C] 
        
        // PRINT TEMPERATURE VALUE
        Serial.print(temp); }
      else { Serial.print(420); };
        
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// SET RELAY OUTPUT
    case SET_RELAY:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt(); // GET CMD RELAY INDEX
      tmpInt[1] = serialMsg.message.sParameter[1].toInt(); // GET CMD RELAY OUTPUT
      
      // SET RELAY OUTPUT
      if(tmpInt[1] == 0){ relayboard[tmpInt[0]].set(false);}
      else if (tmpInt[1] == 1){ relayboard[tmpInt[0]].set(true);};
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// ENABLE/DISABLE LAMP PWM
    case ENABLE_LAMP:
      delay(2);   // DELAY FOR SERIAL COMM
      tmpInt[0] = bool(serialMsg.message.sParameter[0].toInt());    // GET CMD INDEX
      tmpBool[0] = bool(serialMsg.message.sParameter[1].toInt());   // GET CMD ENABLE BIT

      // ENABLE LAMP
      lamp[tmpInt[0]].enableOutput(tmpBool[0]);     // ENABLE OUTPUT TO LAMP
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// SET LAMP PWM OUTPUT
    case SET_LAMP:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();  // GET CMD INDEX
      tmpString = serialMsg.message.sParameter[1];          // GET CMD RGBW STRING
      tmpInt[1] = serialMsg.message.sParameter[2].toInt();  // GET CMD PWM OUTPUT VALUE

      // CYCLE THROUGH RGBW STRING PARAMETER & SET OUTPUT
      for(int i=0; i<=tmpString.length()-1; i++){
        tmpChar[0] = tmpString[i]; // NEW CHAR
        // SET PWM FOR CHANNEL
        if(tmpChar[0] == 'R'){ lamp[tmpInt[0]].set(R, tmpInt[1]);}
        else if(tmpChar[0] == 'G'){ lamp[tmpInt[0]].set(G, tmpInt[1]);}
        else if(tmpChar[0] == 'B'){ lamp[tmpInt[0]].set(B, tmpInt[1]);}
        else if(tmpChar[0] == 'W'){ lamp[tmpInt[0]].set(W, tmpInt[1]);}
      }
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// PRINT ACTUAL OUTPUT VALUE OF LAMP
    case GET_LAMP:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();  // GET CMD INDEX

      // PRINT CURRENT LAMP OUTPUT
      Serial.print(lamp[tmpInt[0]].getStatus()); 
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// ENABLE/DISABLE PUMP PWM OUTPUT
    case ENABLE_PUMP:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();         // GET CMD INDEX
      tmpBool[0] = bool(serialMsg.message.sParameter[1].toInt());  // GET CMD ENABLE BIT

      // SET PUMP OUTPUT
      pump[tmpInt[0]].enableOutput(tmpBool[0]);
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// SET PUMP PWM OUTPUT
    case SET_PUMP:
      delay(2);   // DELAY FOR SERIAL COMMS
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();         // GET CMD INDEX
      tmpInt[1] = serialMsg.message.sParameter[1].toInt();         // GET CMD PWM VALUE
      tmpBool[0] = bool(serialMsg.message.sParameter[2].toInt());  // GET CMD ENABLE BIT

      // SET OUTPUT
      pump[tmpInt[0]].setPWM(byte(tmpInt[1]));
      pump[tmpInt[0]].enableOutput(tmpBool[0]);
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// GET ACTUAL PUMP PWM OUTPUT
    case GET_PUMP:
      delay(2);   // DELAY FOR SERIAL COMMS
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();  // GET CMD INDEX
      tmpInt[1] = pump[tmpInt[0]].getStatus();              // GET CMD CURRENT PUMP OUTPUT

      // PRINT CURRENT PUMP OUTPUT
      Serial.print(tmpInt[1]);       
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// SET BIAS RESISTANCE FOR TC
    case SET_TEMP_RC:
      delay(2);
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();  // GET CMD INDEX
      tmpInt[1] = serialMsg.message.sParameter[1].toInt();  // GET CMD RC-VALUE
      
      // SET BIAS RESISTANCE VALUE
      rc[tmpInt[0]] = tmpInt[1];
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// PRINT HELP SEQUENCE
    case HELP:
      delay(2);
      printHelp();
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;

 // DEFAULT
    case NO_COMMAND:
      delay(2);
      Serial.println("SLAVE_CMD_ERR");
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
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
  Serial.println("   ENABLE_LAMP  ( index[0-1], enable[0/1] )");
  Serial.println("   SET_LAMP     ( index[0-1], colour[R,B,G,W],  value[0-255], enable[0/1] )");
  Serial.println("   GET_LAMP     ( index[0-1] )");
  Serial.println("   ENABLE_PUMP  ( index[0-1], enable[0/1] )"); 
  Serial.println("   SET_PUMP     ( index[0-1], value[0-255],   enable[0/1] )"); 
  Serial.println("   GET_PUMP     ( index[0-1] )"); 
  Serial.println("   SET_RELAY    ( index[0-7],   value[0/1] )");
  Serial.println("   GET_TEMP     ( index[0-1] )");
  Serial.println("   SET_TEMP_RC  ( index[0-1],   biasResitance[...] )");
  Serial.println("   GET_MOISTURE ( index[0-1] )");
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("DEVICE CONNECTIONS");
  Serial.println("");
  
  for(int n=0;n<NR_MOISTURE; n++){
    moisture[n].help();
    moisturePower[n].help();
    Serial.println("");
    }
  
  for(int n=0;n<NR_PUMP; n++){
    pump[n].help();
    vlotter[n].help();
    Serial.println("");
    }
    
  for(int n=0;n<NR_RELAY; n++){
    relayboard[n].help(); 
    Serial.println("");
    }
    
  for(int n=0;n<NR_LAMP; n++){
    lamp[n].help();
    Serial.println("");
    }
    
  for(int n=0;n<NR_TC; n++){ 
    thermocouple[n].help();
    Serial.println("");
    }
  
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("====================================================");
  Serial.print('@');
}
