// https://www.instructables.com/id/Arduino-Timer-Interrupts/

class TimeKeeper{
  public:
    void init();
    void interrupt();
    void set_time();
    String get_time();
    
    int hour = 21; 
    int minute= 44; 
    int second = 0;

  private:
    long int PAR_CLK_IO = 16000000; // 16 MHz
    
    int PAR_PRESCALER = 1024;
    int PAR_CS2 = 7;  // CS2=7 -> 1024 prescaler
    float PAR_CLK_T2 = float( PAR_CLK_IO ) / float(PAR_PRESCALER);
    
    int PAR_OCR2A = 243;
    float PAR_CLK_T2I = PAR_CLK_T2 / float(PAR_OCR2A);  // INTERRUPT TIMER FREQUENCY
    
    int freq_aprox = 64;  // PRESCALER & OCR FREQUENCY APPROXIMATIOn
    float sec_loss = 0.000073;
    
    unsigned long int long_second = 0;
    int cnt_trig2 = 0;
    float sum_loss = 0;
  
} myTimeKeeper;

void TimeKeeper::init(){

      freq_aprox = floor(PAR_CLK_T2I);
      sec_loss = freq_aprox - (1/PAR_CLK_T2I);
      cli();//stop interrupts
      
      // INITIALIZE REGISTERS
      TIMSK2 = 0;
      TCNT2  = 0;
      TCCR2A = 0;
      TCCR2B = 0;

      TCCR2A |= (1 << WGM21);  // turn on CTC mode
      
      GTCCR |= (1 << PSRASY); // RESET PRESCALER

      TCCR2B |= (1 << CS20);   // set pre scalar
      TCCR2B |= (1 << CS21);   // set pre scalar
      TCCR2B |= (1 << CS22);   // set pre scalar
    
      OCR2A = 243;  // set overflow value
      
      TIMSK2 |= (1 << OCIE2A);  // enable timer compare interrupt
      
      TCNT2  = 0;//initialize counter value aigain  to be sure
      sei();//allow interrupts
    };

void TimeKeeper::interrupt(){
  cnt_trig2 += 1;
  sum_loss += sec_loss;
  if (sum_loss >=1){
    // leap second
    long_second -= 1;
    second -= 1;
    sum_loss -= 1;
    Serial.println(long_second);
  }
  
  if (cnt_trig2 >= freq_aprox){
    // 64 Hz aproximation cycle
    long_second += 1;
    second += 1;
    cnt_trig2 = 0;
    Serial.println(long_second);
    Serial.println(sum_loss);
  }

  // DO HHMMSS
  if(second >= 60){
    second  -= 60;
    minute  += 1;
  }
  if(minute >= 60){
    minute  -= 60;
    hour    += 1;
  }
  if(hour >= 24){
    hour  -= 24;
  }
  if (cnt_trig2 == 0) {
    Serial.print("Time:   ");
    Serial.print(hour);
    Serial.print(":");
    Serial.print(minute);
    Serial.print(":");
    Serial.print(second);
    Serial.print("\n\r");
  }
  if (long_second == 4294967280){
  // maximum amount of minutes to fit in long int 
    long_second = 0;
  }
};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  myTimeKeeper.init();
}



ISR(TIMER2_COMPA_vect){
  myTimeKeeper.interrupt();
}

void loop() {
  // put your main code here, to run repeatedly:
  
}
