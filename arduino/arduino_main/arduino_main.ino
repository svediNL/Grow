//#include "comms.h"
//#include "sensors.h" 
//#include "actuators.h"
#include "grow.h" 



Comms serialMsg;
int counter = 0;
bool bNewMessage = false;

String serialString;

Grow grow;

bool x;

void setup(){
  // INIT SERIAL
  Serial.begin(115200);
  grow.init();
  
}

ISR(TIMER2_COMPA_vect){
// ON COUNTER OUTPUT COMPARE TRIGGER
  grow.masterClock.interrupt();
}

void loop()
// MAIN LOOP
{
  if(ENABLE_PUMP_INTERLOCK_SWITCH)
  // CHECK FLOAT SWITCH FOR INTERLOCK
  {
    for(int n=0; n<NR_FLOAT_SWITCH; n++)
    // CYCLE FLOAT SWITCHES
    {
      if( grow.vlotter[n].state() && !grow.overrule_pump_interlock[ FLOAT_PUMP_INTERLOCK_LINKING[n] ] ) 
      // FLOAT SWITCH CLOSED  &  PUMP LINKED TO SWITCH HAS NO OVERRULE INTERLOCK
      { grow.pump[n].interlock(true); }
      else
      // RELEASE INTERLOCK
      { grow.pump[n].interlock(false); };
    };
  }
  
  // DIM LAMP WHEN DOOR OPENS
  if (grow.lamp[0].getStatus()>0 && ENABLE_FRIDGE_DOOR){
  // LAMP IS ON 
    if(grow.doorSensor.state() == true ){
    // DOOR IS OPEN
      for(int n=0; n<4; n++){
         analogWrite(grow.lamp[0].pinRGBW[n], 30); // MANUALLY SET INTESTITY TO 30
      }
      x = true;
    }
    else if(x){
    // DOOR IS CLOSED BUT INTENSITY IS STILL REDUCED
      for(int n=0; n<4; n++){
         analogWrite(grow.lamp[0].pinRGBW[n], grow.lamp[0].valRGBW[n]); // RESET INTESTITY
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
      grow.moisturePower[tmpInt[0]].set(true);    // enable power
      delay(10);                  // let the power settle
      grow.moisture[tmpInt[0]].refresh();         // get value
      grow.moisturePower[tmpInt[0]].set( false);  // disable power

      // PRINT VALUE
      Serial.print(grow.moisture[tmpInt[0]].getMetricValue()); //print raw value
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// PRINT TEMPERATURE VALUE
    case GET_TEMP:
      // GET TC MEASUREMENT
      delay(2); // DELAY SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();  // GET CMD INDEX
      
      grow.thermocouple[tmpInt[0]].refresh();                    // UPDATE TC VALUE
      grow.vm = grow.thermocouple[tmpInt[0]].getMetricValue();        // TRANSLATE TO MEASURED VOLTAGE
      
      if (grow.vin-grow.vm != 0) { // PREVENT DIVIDE BY ZERO
        grow.rntc = (grow.vm*grow.rc[tmpInt[0]])/(grow.vin-grow.vm);                 //GET RESISTANCE OF THERMOCOUPLE 

        // TRANSFORM RESISTANCE TO TEMPERATURE
        grow.temp = grow.rntc / grow.Rn;                                   // A   =   Rntc/Rn    [-]
        grow.temp = log(grow.temp);                                   // tmp =   ln(Rntc/Rn)    [-]
        grow.temp /= grow.coeffB;                                     // tmp =   ln(Rntc/Rn) / coeff   = Tntc^-1 - Tn^-1   [K]
        grow.temp += 1 / (grow.Tn +273.15);                           // tmp = Tntc^-1  [K]
        grow.temp = 1/ grow.temp;                                     // tmp = Tntc   [K]
        grow.temp -= 273.15;                                     // tmp = Tntc   [C] 
        
        // PRINT TEMPERATURE VALUE
        Serial.print(grow.temp); }
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
      if(tmpInt[1] == 0){ grow.relayboard[tmpInt[0]].set(false);}
      else if (tmpInt[1] == 1){ grow.relayboard[tmpInt[0]].set(true);};
      
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
      grow.lamp[tmpInt[0]].enableOutput(tmpBool[0]);     // ENABLE OUTPUT TO LAMP
      
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
        if(tmpChar[0] == 'R'){ grow.lamp[tmpInt[0]].set(R, tmpInt[1]);}
        else if(tmpChar[0] == 'G'){ grow.lamp[tmpInt[0]].set(G, tmpInt[1]);}
        else if(tmpChar[0] == 'B'){ grow.lamp[tmpInt[0]].set(B, tmpInt[1]);}
        else if(tmpChar[0] == 'W'){ grow.lamp[tmpInt[0]].set(W, tmpInt[1]);}
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
      if(grow.doorSensor.state() == true ){
        Serial.print("30");
      }
      else{ Serial.print(grow.lamp[tmpInt[0]].getStatus()); }
      
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
      grow.pump[tmpInt[0]].enableOutput(tmpBool[0]);
      
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
      grow.pump[tmpInt[0]].setPWM(byte(tmpInt[1]));
      grow.pump[tmpInt[0]].enableOutput(tmpBool[0]);
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

// GET ACTUAL PUMP PWM OUTPUT
    case GET_PUMP:
      delay(2);   // DELAY FOR SERIAL COMMS
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();  // GET CMD INDEX
      tmpInt[1] = grow.pump[tmpInt[0]].getStatus();              // GET CMD CURRENT PUMP OUTPUT

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
      grow.rc[tmpInt[0]] = tmpInt[1];
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

    case IGNORE_PUMP_INTERLOCK:
      delay(2);
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();  // GET CMD INDEX
      tmpBool[0] = bool(serialMsg.message.sParameter[1].toInt());  // GET CMD BOOL

      // SET OVERRULE FLAG
      grow.overrule_pump_interlock[ tmpInt[0] ] = tmpBool[0];
      
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
    case SET_CLOCK:
      delay(2); // DELAY FOR SERIAL COMM
      // ACTION
      grow.masterClock.set_time(serialMsg.message.sParameter[0]);
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

   // PRINT HH:MM:SS TIME
    case GET_CLOCK:
      delay(2); // DELAY FOR SERIAL COMM
      // ACTION
      Serial.print(grow.masterClock.get_time());
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

   // PRINT EPOCH SECONDS
    case GET_EPOCH:
      delay(2); // DELAY FOR SERIAL COMM
      // ACTION
      Serial.print(grow.masterClock.get_epoch());

      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

   // RETURN FIRST TIMER AVAILABLE
    case TIMER_CLAIMED:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();         // GET CMD INDEX
      
      Serial.print( grow.masterClock.request_timer());
      
      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

   // CHECK IF CLOCK HAS FINISHED
    case TIMER_OUTPUT:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();         // GET CMD INDEX
      
      Serial.print(int(grow.masterClock.timer_done(tmpInt[0])));

      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

    // CLAIM A TIMER
    case CLAIM_TIMER:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();         // GET CMD INDEX   

      Serial.print(int( grow.masterClock.claim_timer(tmpInt[0]) ));

      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

    // RELEASE TIMER
    case RELEASE_TIMER:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();         // GET CMD INDEX   

      grow.masterClock.release_timer(tmpInt[0]);

      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

    // RESET TIMER
    case RESET_TIMER:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();         // GET CMD INDEX   

      grow.masterClock.reset_timer(tmpInt[0]);

      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;

    // STOP TIMER
    case STOP_TIMER:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();         // GET CMD INDEX   

      grow.masterClock.stop_timer(tmpInt[0]);

      // COMMAND DONE
      serialMsg.message.inputCommand= NO_COMMAND;   // reset command variable
      Serial.print('@');                            // PRINT EOL
      break;


    // SET A CLOCK TO GO OFF AFTER x SECONDS {AKA TIMER}
    case SET_TIMER:
      delay(2); // DELAY FOR SERIAL COMM
      tmpInt[0] = serialMsg.message.sParameter[0].toInt();         // GET CMD INDEX
      tmpInt[1] = serialMsg.message.sParameter[1].toInt();         // GET CMD INDEX

      grow.masterClock.start_timer(byte(tmpInt[0]), tmpInt[1]);
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
  Serial.println("");
  Serial.println("  COMMAND(PAR1, PAR2, PAR3, ETC)\n");
  Serial.println("  example:   SET_LAMP(0, RB, 128), will set the Red and Blue channels to 128 for lamp 0");
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("");
  Serial.print("NR_LAMP:  ");Serial.print(NR_LAMP);Serial.print("\n");
  Serial.print("NR_PUMP:  ");Serial.print(NR_PUMP);Serial.print("\n");
  Serial.print("NR_RELAY:  ");Serial.print(NR_RELAY);Serial.print("\n");
  Serial.print("NR_TC:  ");Serial.print(NR_TC);Serial.print("\n");
  Serial.print("NR_MOISTURE:  ");Serial.print(NR_MOISTURE);Serial.print("\n");
  Serial.println("");
  Serial.println("List of commands:");

  Serial.println("   ENABLE_LAMP  ( index[0..NR_LAMP-1], enable[0/1] )");
  Serial.println("   SET_LAMP     ( index[0..NR_LAMP-1], colour[R,B,G,W],  value[0-255], enable[0/1] )");
  Serial.println("   GET_LAMP     ( index[0..NR_LAMP-1] )");

  Serial.println("   ENABLE_PUMP  ( index[0..NR_PUMP-1], enable[0/1] )"); 
  Serial.println("   SET_PUMP     ( index[0..NR_PUMP-1], value[0-255],   enable[0/1] )"); 
  Serial.println("   GET_PUMP     ( index[0..NR_PUMP-1] )"); 

  Serial.println("   IGNORE_PUMP_INTERLOCK ( index[0..NR_PUMP-1], enable[0/1] )");

  Serial.println("   SET_RELAY    ( index[0..NR_RELAY-1],   value[0/1] )");

  Serial.println("   GET_TEMP     ( index[0..NR_TC-1] )");
  Serial.println("   SET_TEMP_RC  ( index[0..NR_TC-1],   biasResistance[...ohm] )");

  Serial.println("   GET_MOISTURE ( index[0..NR_MOISTURE-1] )");

  Serial.println("   SET_CLOCK   ( time[HH:MM:SS] )");
  Serial.println("   GET_CLOCK   ( )");
  Serial.println("   GET_EPOCH  ( )");

  Serial.println("   TIMER_OUTPUT   ( index[0..NR_TIMER] )");
  Serial.println("   TIMER_CLAIMED  ( index[0..NR_TIMER] )");
  Serial.println("   CLAIM_TIMER       ( index[0..NR_TIMER] )");
  Serial.println("   SET_TIMER         ( index[0..NR_TIMER], time[...s] )");
  Serial.println("");
  Serial.println("");
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("D E V I C E    C O N N E C T I O N S");
  Serial.println("");

  Serial.println("- MOISTURE SENSORS");
  for(int n=0;n<NR_MOISTURE; n++){
    grow.moisture[n].help();
    grow.moisturePower[n].help();
    }
  Serial.println("");

  Serial.println("- PUMPS");
  for(int n=0;n<NR_PUMP; n++){
    grow.pump[n].help();
    grow.vlotter[n].help();
    }
  Serial.println("");

  Serial.println("- RELAYS");
  for(int n=0;n<NR_RELAY; n++){
    grow.relayboard[n].help(); 
    }
  Serial.println("");

  Serial.println("- LAMPS");
  for(int n=0;n<NR_LAMP; n++){
    grow.lamp[n].help();
    }
  Serial.println("");

  Serial.println("- TEMPERATURE SENSORS");
  for(int n=0;n<NR_TC; n++){ 
    grow.thermocouple[n].help();
    }
  Serial.println("");
  
  Serial.println(" - - - - - - - - - - - - - - - - - - ");
  Serial.println("");
  Serial.println("====================================================");
  Serial.print('@');
}
