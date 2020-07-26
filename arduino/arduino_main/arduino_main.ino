#include "grow.h" 

Grow grow;

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
  grow.doStuff();
}
 
void serialEvent(){
  grow.serialString = Serial.readStringUntil('\n');
  grow.bNewMessage = true;
}
