# Grow
This project uses a `Python` program in combination with an `Arduino Mega` to monitor and control factors that are involved with plant growth.

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

On the microcontroller, the following devices can be configured:
- X amount of `moisture sensor`s [Analog Input, Digital Output] 
- X amount of h-brigde `pump`s [2x PWM Outout]
- X amount of water level `float switch`es [Digital Input]
- X amount of `valve relay`s [Digital Output]
- X amount of `NTC thermistor`s [Analog Input]
- X amount of RGBW-channel `LED driver`s [PWM Output]
- Light dimming door switch [Digital Input]

## /Grow
Software suite for plant environment control.

## /Grow/app
Application directory for main application. 

### /Grow/app/config.py
Configuration of the grow setup. 
Device can be defined here and must be in accordance with the configuration installed on the arduino slave (grow.h)

### /Grow/app/gui.py
Main program.

Run in terminal using: `~/Grow/app$ python gui.py`

Dependencies: `matplotlib`, `tkinter`

### /Grow/app/comms.py
Custom library for communication with arduino.

Dependencies: `pySerial`

## /Grow/arduino

### /Grow/arduino/grow.h
Devices are defined here.

## Installing python modules
### matplotlib
`pip install matpotlib`

### pySerial
`pip install pyserial`
``
