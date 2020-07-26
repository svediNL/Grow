#ifndef TIMEKEEPING_H
#include "timekeeping.h"

void TimeKeeper::set_base_time(long int var)
{
  PAR_CLK_IO = var;   // SET BASE TIME
  // CALCULATE FRQUENCY STUFF
  PAR_CLK_T2 = double( PAR_CLK_IO ) / double(PAR_PRESCALER);
  PAR_CLK_T2I = PAR_CLK_T2 / double(PAR_OCR2A+1);
  freq_aprox = floor(PAR_CLK_T2I);
  sec_loss = (1/double(freq_aprox)) - (1/double(PAR_CLK_T2I));
};

void TimeKeeper::set_base_prescaler(int var)
{
  PAR_PRESCALER = var;  // SET PRESCALER
  // CALCULATE FREQUENCY STUFF
  PAR_CLK_T2 = double( PAR_CLK_IO ) / double(PAR_PRESCALER);
  PAR_CLK_T2I = PAR_CLK_T2 / double(PAR_OCR2A+1);
  freq_aprox = floor(PAR_CLK_T2I);
  sec_loss = (1/double(freq_aprox)) - (1/double(PAR_CLK_T2I));
};

void TimeKeeper::set_output_compare(int var)
{
  PAR_OCR2A = var;  // SET OUTPUT COMPATE VALUE
  // CALCULATE FREQUENCY STUFF
  PAR_CLK_T2 = double( PAR_CLK_IO ) / double(PAR_PRESCALER);
  PAR_CLK_T2I = PAR_CLK_T2 / double(PAR_OCR2A+1);
  freq_aprox = floor(PAR_CLK_T2I);
  sec_loss = (1/double(freq_aprox)) - (1/double(PAR_CLK_T2I));
};

void TimeKeeper::set_time(String var)
{
  String tmp = "";  // TMP STRING
  int cnt = 0;      // COUNTER FOR HH:MM:SS

  for(int i=0; i<=var.length(); i++)
  // CYCLE THROUGH CHARS IN STRING
  {
    if (cnt<3)
    // NOT YET ALL TIME DIVISION HAD
    {
      if(var[i]!=':' && var[i]!='.' && var[i]!=' ')
      {
      // FILTER SEPERATORS
        tmp += var[i];  // ADD CHAR TO STRING
      };
          
      if( var[i]==':' || i==var.length()-1 )
      // SEPERATOR OR END OF TIME REACHED
      {
        switch(cnt)
        // ADD HH MM SS ONE BY ONE
        {
          case 0:
            hour = tmp.toInt();
            break;
          case 1:
            minute = tmp.toInt();
            break;
          case 2:
            second = tmp.toInt();
            break;
        };
        tmp = "";
        cnt++;
      }
    }
    else
    // HH:MM:SS HAS BEEN FILLED
    {
      break;
    };
  };
};

void TimeKeeper::set_magic_comp(unsigned long int var){ magic_time_comp = var; };

void TimeKeeper::init()
{
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

void TimeKeeper::interrupt()
{
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
    epoch_toggle = !epoch_toggle;
  }
};

unsigned long int TimeKeeper::get_epoch(){ return long_second; };

String TimeKeeper::get_time()
{
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

void TimeKeeper::print_parameters()
{
  Serial.println(PAR_CLK_T2 );
  Serial.println(PAR_CLK_T2I);
  Serial.println(freq_aprox);
  Serial.println(String(sec_loss, 10)) ;
};

int   TimeKeeper::request_timer()
{
  for(int n=0; n<10;n++){
    if(!subTimers[n].is_claimed){
      return n;
      break;
    }
  }
};

bool TimeKeeper::claim_timer(byte index)
{
  return subTimers[index].claim();
};

void TimeKeeper::release_timer(byte index)
{
  subTimers[index].stop();
  subTimers[index].release();  
};

void TimeKeeper::start_timer(byte index, int time_par)
{
  subTimers[index].start(long_second, time_par);
};

void TimeKeeper::reset_timer(byte index)
{
  subTimers[index].reset(long_second);
};

void TimeKeeper::stop_timer(byte index)
{
  subTimers[index].stop();
};

bool TimeKeeper::timer_done(byte index)
{
  return subTimers[index].output(long_second);
};


// SubTimer::
bool SubTimer::output(unsigned long int current_ep)
// 
{
  return is_claimed * is_running * ((current_ep - start_time) >= trig_time);
};

void SubTimer::start(unsigned long int current_ep, unsigned long int time_par)
{
  start_time = current_ep;
  trig_time = time_par;
  is_running = true;
};

void SubTimer::reset(unsigned long int current_ep)
{
  start_time = current_ep;
};

void SubTimer::stop(){
  is_running = false;
};

bool SubTimer::claim(){
  if(!is_claimed){
    is_claimed = true;
    return true;
  }
  else{ return false;};
};

bool SubTimer::release(){
  if(!is_running){
    is_claimed = false;
    return true;  
  }
  else{ return false;};
};
#endif
