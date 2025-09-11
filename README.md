# Anti-Sleep Alarm for Drivers (Raspberry Pi)

This project is a Python implementation of an **anti-sleep alarm** designed to alert a driver when their eyes remain closed for too long.  
It uses an IR eye-detection sensor, a buzzer, and a small motor (or vibration motor) connected to a Raspberry Pi.

## Features
- **Eye-closure detection**: IR sensor monitors if the driver’s eyes are closed.
- **Timed response**:  
  - Buzzer sounds if eyes stay closed for **3 seconds**.  
  - Motor switches off after **4 seconds** to conserve power.
- **Fail-safe cleanup**: GPIO pins are reset on exit.

## Hardware Requirements
- Raspberry Pi (any model with GPIO headers)
- IR or eye-detection sensor (active-low output)
- Buzzer (active-high)
- Motor or vibration motor with appropriate driver/relay
- Jumper wires and power supply



## Installation
1. **Enable GPIO** on your Raspberry Pi (enabled by default on Raspberry Pi OS).
2. Install Python 3 and the GPIO library:
   ```bash
   sudo apt update
   sudo apt install python3 python3-rpi.gpio



✔The code I have pushed is basically the conversion from arduino to Python before moving to Raspberry Pi.


**NEXT STEPS**
✔What is needed is for you guys to check it, and then we'll have to implement the dashboard code with tkInter

✔Connect the dashboard with tkInter.
✔Link it with this python code
✔Move this code to Raspberry Pi