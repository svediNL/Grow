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
  rc = 14700;
  vin = 5.0;
  Tn = 25;
  Rn = 10000;
  coeffB=3435;
  Serial.begin(115200);
  Serial.println(" + = + = + = +   + = + = + = +   + = + = + = +");
  delay(750);  
  Serial.print("Booting grow controller");
  for( int n=0; n<3; n++){
    Serial.print(".");
    delay(333);  
  }
  Serial.print("\n\r");
  Serial.println("");
  
  lamp.init("RGBW LED PWM output",11,10,9,8);
  pump.init(7,6,"pump on H-Bridge board");

  moisture.init(A0, "water sensor - analog input", 1023, 100, "%");
  thermocouple.init(A1, "thermocouple", 1023, 5, "V");
  
  moisturePower.init(22, "water sensor - power enable");
  relayboard[0].init(24, "relay0");
  relayboard[1].init(26, "relay1");

  vlotter.init(23, "vlotter");

  Serial.println(" + = + = + = +   + = + = + = +   + = + = + = +");
  Serial.println("Running");
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
  int iTmpPar[4];
  bool bTmpPar[4];
  String tmpString;
  char tmpChar;
  int tmpInt;
  bool tmpBool;
  switch(serialMsg.message.inputCommand){

    case GET_MOISTURE:
      moisturePower.set(true); // enable power
      delay(10);  // let the power settle
      moisture.refresh(); // get value
      moisturePower.set( false);  // disable power

      Serial.print(moisture.getRawValue()); //print raw value
      Serial.print("\n"); // close line
      
      serialMsg.message.inputCommand= -1; // reset command variable
      break;

    case GET_TEMP:
    
      thermocouple.refresh();
      vm = thermocouple.getMetricValue();
      if (vin-vm != 0) {
        rntc = (vm*rc)/(vin-vm);
      
        temp = rntc / Rn;
        temp = log(temp);
        temp /= coeffB;
        temp += 1 / (Tn +273.15);
        temp = 1/ temp;
        temp -= 273.15;
        
        Serial.print(temp);
        Serial.print("\n");
      }
      else { 
        Serial.print(420);
        Serial.print("\n");
        };
      serialMsg.message.inputCommand= -1; // reset command variable
      break;
      
    case SET_RELAY:
      //Serial.println("ACK");
      tmpInt = serialMsg.message.sParameter[0].toInt();
      Serial.println(tmpInt);
      if(serialMsg.message.sParameter[1] == "0"){ relayboard[tmpInt].set(false);}
      else if (serialMsg.message.sParameter[1] == "1"){ relayboard[tmpInt].set(true);};
      serialMsg.message.inputCommand= -1;
      break;
      
    case ENABLE_LAMP:
      //Serial.println("ACK");
      tmpBool = bool(serialMsg.message.sParameter[0].toInt()); 
      lamp.enableOutput(tmpBool);
      serialMsg.message.inputCommand= -1; // reset command variable
      break;
      
    case SET_LAMP:
      //Serial.println("ACK");
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
      serialMsg.message.inputCommand= -1;
      break;
        
    case ENABLE_PUMP:
      //Serial.println("ACK");
      tmpBool = bool(serialMsg.message.sParameter[0].toInt()); 
      pump.enableOutput(tmpBool);
      serialMsg.message.inputCommand= -1;
      break;
      
    case SET_PUMP:
      //Serial.println("ACK");
      tmpInt = serialMsg.message.sParameter[0].toInt();
      tmpBool = bool(serialMsg.message.sParameter[1].toInt());
      
      pump.setPWM(byte(tmpInt));
      pump.enableOutput(tmpBool);
      break;
    
    case HELP:
      serialMsg.printHelp();
      serialMsg.message.inputCommand= -1;
      break;
       
    default:
      Serial.println("COMM_ERR");
      break;
  }
  
}