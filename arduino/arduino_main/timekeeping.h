#ifndef TIMEKEEPING_H
#define TIMEKEEPING_H

#include <Arduino.h>

class SubTimer{
    public:
        void stop();
        void start(unsigned long int current_ep, unsigned long int time_par);
        void reset(unsigned long int current_ep);
        bool output(unsigned long int current_ep);

        bool claim();
        bool release();

        bool is_claimed = false;
        bool is_running = false;


    private:
        unsigned long int start_time;
        unsigned long int current_time;
        unsigned long int trig_time;
};


class TimeKeeper{
  public:
    void set_base_time(long int var);
    void set_base_prescaler(int var);
    void set_output_compare(int var);
    
    void set_time(String var);
    void set_magic_comp(unsigned long int var);
    
    void init();
    void interrupt();
    
    unsigned long int get_epoch();
    String get_time();

    int request_timer(); // returns -1 when none available
    bool claim_timer(byte index);
    void release_timer(byte index);
    void start_timer(byte index, int time_par);
    void reset_timer(byte index);
    void stop_timer(byte index);
    bool timer_done(byte index);

    
    void print_parameters();
    bool epoch_toggle;

  private:
    //const int   NR_TIMERS = 10;
    long int PAR_CLK_IO = 16000000;   // BASE TIMER CLOCK FREQUENCY -> 16 MHz
    
    int PAR_PRESCALER = 1024;         // BASE TIMER PRE-SCALER VALUE
    int PAR_CS2 = 7;                  // CSn REGISTER VALUE TO SELECT PRE_SCALER ->  CS2=7 -> 1024 prescaler
    
    int PAR_OCR2A = 243;              // OUTPUT COMPARE VALUE -> TRIGGER ISR(TIMERn_COMPx_vect){} WHEN COUNTER REACHES VALUE
    
    double PAR_CLK_T2 = double( PAR_CLK_IO ) / double(PAR_PRESCALER);   // COUNTER FREQUENCY -> BASE TIME WITH PRE-SCALER
    double PAR_CLK_T2I = PAR_CLK_T2 / double(PAR_OCR2A+1);              // ISR INTERRUPT FREQUENCY -> OUTPUT COMPARE FREQUENCY
    
    int freq_aprox = 64;  // ISR INTERRUPT FREQUENCY APPROXIMATIOn
    double sec_loss = 0;  // TIMER - APPROX PERIOD DIFFERENCE

    unsigned long int magic_time_comp = 6379; // COMPENSATION SECOND FOR MAGIC DRIFT 

    int cnt_trig2 = 0;                        // COUNTER FOR ISR INTERRUPT -> TRIGGER SECOOND APPROX WHEN VALUE REACHES freq_aprox
    double sum_loss = 0;                      // TRACK TIME DIFFERENCE DUE TO APPROXIMATIONS
    unsigned long int long_second = 0;        // EPOCH SECOND TIMER

    int hour = 1; 
    int minute= 2; 
    int second = 3;
    SubTimer subTimers[10];
};
#endif
