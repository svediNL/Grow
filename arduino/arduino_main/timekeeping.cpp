#ifndef TIMEKEEPING_H
#include "timekeeping.h"

void TimeKeeper::set_base_time(long int var){
  PAR_CLK_IO = var; 
  PAR_CLK_T2 = double( PAR_CLK_IO ) / double(PAR_PRESCALER);
  PAR_CLK_T2I = PAR_CLK_T2 / double(PAR_OCR2A+1);
  freq_aprox = floor(PAR_CLK_T2I);
  sec_loss = (1/double(freq_aprox)) - (1/double(PAR_CLK_T2I));
};

void TimeKeeper::set_base_prescaler(int var){
  PAR_PRESCALER = var;
  PAR_CLK_T2 = double( PAR_CLK_IO ) / double(PAR_PRESCALER);
  PAR_CLK_T2I = PAR_CLK_T2 / double(PAR_OCR2A+1);
  freq_aprox = floor(PAR_CLK_T2I);
  sec_loss = (1/double(freq_aprox)) - (1/double(PAR_CLK_T2I));
};
void TimeKeeper::set_output_compare(int var){
  PAR_OCR2A = var;
  PAR_CLK_T2 = double( PAR_CLK_IO ) / double(PAR_PRESCALER);
  PAR_CLK_T2I = PAR_CLK_T2 / double(PAR_OCR2A+1);
  freq_aprox = floor(PAR_CLK_T2I);
  sec_loss = (1/double(freq_aprox)) - (1/double(PAR_CLK_T2I));
};

void TimeKeeper::set_time(String var){
  String tmp = "";
  int cnt = 0;
  for(int i=0; i<=var.length(); i++)
  {
    if (var[i]=':' && cnt<3)
    {
      switch(cnt){
        case 0:
          second = tmp.toInt();
          break;
        case 1:
          minute = tmp.toInt();
          break;
        case 2:
          hour = tmp.toInt();
          break;
        default:
          break;
      }
      tmp = "";
      cnt++;
    }
    else if (cnt >= 3)
    {
      break;
    }
    else
    {
      tmp += var[i];
    };
  };
};

void TimeKeeper::set_magic_comp(unsigned long int var){
  magic_time_comp = var;
};

void TimeKeeper::init(){
      PAR_CLK_T2 = double( PAR_CLK_IO ) / double(PAR_PRESCALER);
      PAR_CLK_T2I = PAR_CLK_T2 / double(PAR_OCR2A+1);
      freq_aprox = floor(PAR_CLK_T2I);
      sec_loss = (1/double(freq_aprox)) - (1/double(PAR_CLK_T2I));
      
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
  
  if (cnt_trig2 >= freq_aprox)
  {
    // 64 Hz aproximation cycle
    long_second += 1;
    second += 1;
    cnt_trig2 = 0;

    if ((long_second%magic_time_comp) == 0 && long_second>0 && magic_time_comp != 0)
    {
      Serial.println("magic leap second");
      second -= 1;
    }
    
    Serial.println(long_second);
    Serial.println(sum_loss);
  }

  if (abs(sum_loss) >=1)
  {
    // leap second
    Serial.println("leap second");
    if (sum_loss >0)
    {
      long_second += 1;
      second += 1;
      sum_loss -= 1;
    }
    else
    {
      long_second -= 1;
      second -= 1;
      sum_loss += 1;
    }
  }

  // DO HHMMSS
  if(second >= 60)
  {
    second  -= 60;
    minute  += 1;
  }
  if(minute >= 60)
  {
    minute  -= 60;
    hour    += 1;
  }
  if(hour >= 24)
  {
    hour  -= 24;
  }
  if (cnt_trig2 == 0) 
  {
    Serial.print("Time:   ");
    Serial.print(hour);
    Serial.print(":");
    Serial.print(minute);
    Serial.print(":");
    Serial.print(second);
    Serial.print("\n\r");
  }
  if (long_second == 4294967280)
  {
  // maximum amount of minutes to fit in long int 
    long_second = 0;
  }
};

unsigned long int TimeKeeper::get_epoch(){
  return long_second;
};

String TimeKeeper::get_time(){
  String tmp;
  if(hour<10){
    tmp += '0';
  }
  tmp += hour;
  tmp += ':';

  if(minute<10){
    tmp += '0';
  }
  tmp += minute;
  tmp += ':';
  
  if(second<10){
    tmp += '0';
  }
  tmp += second;
  return tmp;
};

void TimeKeeper::print_parameters(){
  Serial.println(PAR_CLK_T2 );
  Serial.println(PAR_CLK_T2I);
  Serial.println(freq_aprox);
  Serial.println(String(sec_loss, 10)) ;
};



#endif
