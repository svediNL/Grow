#include "comms.h"
#include "sensors.h" 
#include "actuators.h"
#include "grow.h" 

bool overrule_pump_interlock[NR_PUMP];

Comms serialMsg;
int counter = 0;
bool bNewMessage = false;

String serialString;

float rntc, vin, vm;
float rc[NR_TC];
float Tn, Rn, coeffB, temp;

bool x;

void setup(){
  // INIT SERIAL
  Serial.begin(115200);

  // SETUP CLOCK
  myClock.set_base_time(16000000);
  myClock.set_base_prescaler(1024);
  myClock.set_output_compare(243);
  myClock.set_time("12:00:00");
  myClock.set_magic_comp(6379);
  myClock.init();
  
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
}

ISR(TIMER2_COMPA_vect){
// ON COUNTER OUTPUT COMPARE TRIGGER
  myClock.interrupt();
}

void loop(){
  if(ENABLE_PUMP_INTERLOCK_SWITCH){
    if(vlotter[0].state() && !overrule_pump_interlock[0]) { pump[0].interlock(true);}
    else { pump[0].interlock(false); };
  }
  
  // DIM LAMP WHEN DOOR OPENS
  if (lamp[0].getStatus()>0 && ENABLE_FRIDGE_DOOR){
    if(doorSensor.state() == true ){
    // DOOR IS OPEN
      for(int n=0; n<4; n++){
         analogWrite(lamp[0].pinRGBW[n], 30); // SET INTESTITY TO 30
      }
      x = true;
    }
    else if(x){
      for(int n=0; n<4; n++){
         analogWrite(lamp[0].pinRGBW[n], lamp[0].valRGBW[n]); // RESET INTESTITY
      }
      x=false;
    }
  }

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
      if(doorSensor.state() == true ){
        Serial.print("30");
      }
      else{ Serial.print(lamp[tmpInt[0]].getStatus()); }
      
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

    case IGNORE_PUMP_INTERLOCK:
      delay(2);
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();  // GET CMD INDEX
      tmpBool[0] = bool(serialMsg.message.sParameter[1].toInt());  // GET CMD BOOL

      // SET OVERRULE FLAG
      overrule_pump_interlock[tmpInt[0]] = tmpBool[0];
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');            
      break;
      

// PRINT HELP SEQUENCE
    case HELP:
      delay(2);
      printHelp();
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND; // reset command variable
      Serial.print('@');
      break;

 // SET HH:MM:SS TIME
    case SET_TIME:
      delay(2); // DELAY FOR SERIAL COMM
      // ACTION
      myClock.set_time(serialMsg.message.sParameter[0]);
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

   // PRINT HH:MM:SS TIME
    case GET_TIME:
      delay(2); // DELAY FOR SERIAL COMM
      // ACTION
      Serial.print(myClock.get_time());
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

   // PRINT EPOCH SECONDS
    case GET_EPOCH:
      delay(2); // DELAY FOR SERIAL COMM
      // ACTION
      Serial.print(myClock.get_epoch());
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;


 // DEFAULT
    case NO_COMMAND:
      delay(2); // DELAY FOR SERIAL COMM
      // ACTION
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
  Serial.println("");
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("- Commands use the following syntax: ");
  Serial.println("  COMMAND(PAR1, PAR2, PAR3, ETC)\n");
  Serial.println("");
  Serial.println("List of commands:");
  Serial.println("   ENABLE_LAMP  ( index[0-x], enable[0/1] )");
  Serial.println("   SET_LAMP     ( index[0-x], colour[R,B,G,W],  value[0-255], enable[0/1] )");
  Serial.println("   GET_LAMP     ( index[0-x] )");
  Serial.println("   ENABLE_PUMP  ( index[0-x], enable[0/1] )"); 
  Serial.println("   SET_PUMP     ( index[0-x], value[0-255],   enable[0/1] )"); 
  Serial.println("   GET_PUMP     ( index[0-x] )"); 
  Serial.println("   SET_RELAY    ( index[0-x],   value[0/1] )");
  Serial.println("   GET_TEMP     ( index[0-x] )");
  Serial.println("   SET_TEMP_RC  ( index[0-x],   biasResitance[...] )");
  Serial.println("   GET_MOISTURE ( index[0-x] )");
  Serial.println("   IGNORE_PUMP_INTERLOCK ( index[0-x], enable[0/1] )");
  Serial.println("");
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("D E V I C E    C O N N E C T I O N S");
  Serial.println("");

  Serial.println("- MOISTURE SENSORS");
  for(int n=0;n<NR_MOISTURE; n++){
    moisture[n].help();
    moisturePower[n].help();
    }
  Serial.println("");

  Serial.println("- PUMPS");
  for(int n=0;n<NR_PUMP; n++){
    pump[n].help();
    vlotter[n].help();
    }
  Serial.println("");

  Serial.println("- RELAYS");
  for(int n=0;n<NR_RELAY; n++){
    relayboard[n].help(); 
    }
  Serial.println("");

  Serial.println("- LAMPS");
  for(int n=0;n<NR_LAMP; n++){
    lamp[n].help();
    }
  Serial.println("");

  Serial.println("- TEMPERATURE SENSORS");
  for(int n=0;n<NR_TC; n++){ 
    thermocouple[n].help();
    }
  Serial.println("");
  
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("");
  Serial.println("====================================================");
  Serial.print('@');
}
