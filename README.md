# Grow
This project uses a `Python` program in combination with an `Arduino Mega` to monitor and control  factors that are involved with plant growth.

It is supposed to be used as an open-source, modular platform for growers that want to find (or create) optimal growing conditions for the growth of their plants.

The main program is started by running `python gui.py`. 
Through GUI:
  - User can choose to enable/diable light as well as control intensity 
      - Manual control
      - Automatic configurable day/night cycle
  - Pump is controlled with a PWM setpoint (0-255) and has external enable/disable button. 
      - The pump is interlocked (meaning it will stop) when the float switch is open, to prevent overflow or keep water at a certain level.
  - Moisture value and temperature values are logged
    - Current values displayed seperatly
    
The project is currently equiped with following devices:
  - Water sensor  (0V-5V)
  - Float switch  (Normally closed, connect to ground)
  - 1 thermistor
  - 2 relay outputs
  - 1 light PWM analog output (PWM used to control LED-current-driver)
  - 1 Pump controlled by PWM H-bridge driver
  

    
## /Grow
Software suite for plant environment control.

## /Grow/app
Application directory for main application. 

### /Grow/app/gui.py
Main program.

Run in terminal using: `~/Grow/app$ python gui.py`

Dependencies: `matplotlib`, `tkinter`

### /Grow/app/comms.py
Custom library for communication with arduino.

Dependencies: `pySerial`

## /Grow/arduino
