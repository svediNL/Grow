// https://www.instructables.com/id/Arduino-Timer-Interrupts/


void setup() {
  // put your setup code here, to run once:
  cli();//stop interrupts

//set timer2 interrupt
  TCCR2A = 0;// set entire TCCR2A register to 0
  TCCR2B = 0;// same for TCCR2B
  TCNT2  = 0;//initialize counter value to 0

  OCR2A = 61;  // set overflow value
  // turn on CTC mode
  TCCR2A |= (1 << WGM21);  // SHIFT BIT INTO REGISTER
  // set pre scalar
  TCCR2B |= (1 << CS20);   
  TCCR2B |= (1 << CS21);   
  TCCR2B |= (1 << CS22);   
  // enable timer compare interrupt
  TIMSK2 |= (1 << OCIE2A);

  sei();//allow interrupts
  Serial.begin(9600);
}

ISR(TIMER2_COMPA_vect){
  Serial.println("Hey");
}

void loop() {
  // put your main code here, to run repeatedly:
  
}
