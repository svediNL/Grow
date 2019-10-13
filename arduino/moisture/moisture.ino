#include "comms.h"
#include "sensors.h" 
#include "actuators.h"

int rawMoisture = 0;

Message inputMessage;
AnalogSensor moisture;

boolean cmdBool = false;
int stage=0;
int parIndex = 0;
String tmpString;

void update_analog_sensor( AnalogSensor *inputSensor, int rawValue ){
  inputSensor->rawValue = rawValue;
  inputSensor->metricValue = (inputSensor->rawValue / inputSensor->rawFullScaleValue ) * inputSensor->metricFullScaleValue;
  inputSensor->percentage = (float(inputSensor->rawValue) / float(inputSensor->rawFullScaleValue) ) * 100;
}

void setup(){
  Serial.begin(9600);
  moisture.rawFullScaleValue = 715;
}

void loop(){
  update_analog_sensor(&moisture, analogRead(A0) );  
  Serial.println(moisture.percentage);
  if (inputMessage.bNewMessage){
    Serial.println(" - - - - - - - - ");
    Serial.println(inputMessage.sInput);
    Serial.println(inputMessage.sCommand);
    Serial.println(inputMessage.sParameter[0]);
    Serial.println(inputMessage.sParameter[1]);
    Serial.println(inputMessage.sParameter[2]);

    inputMessage.bNewMessage = false;
    Serial.flush();
  }
  messageHandler(&inputMessage);
  delay(500);
}
 
void serialEvent(){
  inputMessage.sInput = "";
  parIndex = 0;
  while(Serial.available() && !inputMessage.bNewMessage)
  {
    char inputChar = (char)Serial.read();
    inputMessage.sInput += inputChar;
    
    if (inputChar ==  ':') 
    { 
      stage = 1;
    }
    
    else if (inputChar == ',')
    {
      stage =2;
    }
    else if (inputChar == '\n' || inputChar == '\r')
    { 
      stage =2;
      inputMessage.bNewMessage = true;
    }
    else if (inputChar == ' ')
    {
      stage = 99;
    };
    Serial.print(stage);
    switch(stage)
    {
      case 0:
        //IDLE
        tmpString += inputChar; 
        break;
      case 1:
        //SET COMMAND
        Serial.print("add command: ");
        Serial.print(tmpString);
        Serial.print("\n\r");
        inputMessage.sCommand =tmpString;
        tmpString = "";
        stage = 0;
        break;
      case 2:
        //ADD PARAMETER
        Serial.print("add parameter");
        Serial.print(parIndex);
        Serial.print(": ");
        Serial.print(tmpString);
        Serial.print("\n\r");
        inputMessage.sParameter[parIndex] = tmpString;
        parIndex++;
        tmpString = "";
        stage = 0;
        break;
      case 99:
        //IGNORE CHAR CASE
        stage= 0;
        break;
        
    };
  };
  //Serial.println(inputMessage.sInput);
  Serial.flush();
  
}
