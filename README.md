
# Pico W Ducky 
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/) 

Pico Ducky is a CircuitPython Pico W program that allows you to turn your regular old Pico W into a full working advanced hacking tool just with a few drag and drop actions

I was inspired by [dbisu's](https://github.com/dbisu/) interpretation but was disappointed that I couldn't get it working In this repository you will find everything you need to drag 'n' drop and get started.


## Installation

Firstly you need to drop the [flash_nuke.uf2](https://github.com/bonsall2004/PicoDucky/tree/main/Install%20Tools) into the raspberry pi to clear up any old code that might have been already on the pi
```bash
flash_nuke.uf2
```

Once that has completed you need to drag and drop the [adafruit-circuitpython-raspberry_pi_pico_w-en_US-8.0.3.uf2](https://github.com/bonsall2004/PicoDucky/tree/main/Install%20Tools) Circuit Python uf2 onto the pi to be able to run the code  
```bash
adafruit-circuitpython-raspberry_pi_pico_w-en_US-8.0.3.uf2
```

To deploy the python script all you need to do is drag and drop the [Script](https://github.com/bonsall2004/PicoDucky/tree/main/Script) into the circuit python pico directory

If you want to be able to modify the code after you've added the script file to the pi you will need to ground pin 0 [GP0](https://pico.pinout.xyz/) 

### Notes:
- I have included the circuit python uf2 that I developed with, this install works and your milage may vary if you install directly from circuit python's website yourself.

- You will not be able to view the directory and create custom scripts using the Web GUI at the same time due to read only restrictions in the Pi's FileSystem.

## Deployment
To access the Web GUI you will first need to connect to the network the defaults are 
```bash
SSID: Rasp Pi
Password: Password1234
```

These can be changed in the preferences tab in the Web GUI although you will need to reboot the Pi by unplugging it and replugging it back in.

Once you have connected to the network you will need to navigate to [http://192.168.4.1](http://192.168.4.1)
On the WebGUI you will be able to run, edit and delete scripts along with change the Pi's Preferences such as turning auto run on and off or chosing which script you want to auto run.
## Documentation
These are all acceptable characters
### Modifier keys:
- WINDOWS (Win key)
- GUI (Windows key or Command key on Mac)
- APP (Application key or Menu key)
- SHIFT
- ALT
- CONTROL (or CTRL)

### Arrow keys:
- DOWNARROW (Down arrow key)
- DOWN (Down arrow key)
- LEFTARROW (Left arrow key)
- LEFT (Left arrow key)
- RIGHTARROW (Right arrow key)
- RIGHT (Right arrow key)
- UPARROW (Up arrow key)
- UP (Up arrow key)

### Other keys:
- BREAK (Pause/Break key)
- PAUSE (Pause/Break key)
- CAPSLOCK (Caps Lock key)
- DELETE (Delete key)
- END (End key)
- ESC (Escape key)
- ESCAPE (Escape key)
- HOME (Home key)
- INSERT (Insert key)
- NUMLOCK (Num Lock key)
- PAGEUP (Page Up key)
- PAGEDOWN (Page Down key)
- PRINTSCREEN (Print Screen key)
- ENTER (Enter key)
- SCROLLLOCK (Scroll Lock key)
- SPACE (Spacebar)
- TAB (Tab key)
- BACKSPACE (Backspace key)

### Alphabetic keys:
- A
- B
- C
- D
- E
- F
- G
- H
- I
- J
- K
- L
- M
- N
- O
- P
- Q
- R
- S
- T
- U
- V
- W
- X
- Y
- Z

### Function keys:
- F1
- F2
- F3
- F4
- F5
- F6
- F7
- F8
- F9
- F10
- F11
- F12

### Ducky Commands:
- REM - Comment
- DELAY <time in ms> - Asynchronous Delay
- STRING <text> - Types out a string (can include Numbers)
- PRINT <string> - Prints to the python COM console
- [DEFAULT_DELAY | DEFAULTDELAY] - Runs an Asynchronous Delay for the default time (can be changed in the config.json)
- IMPORT <script> - Imports and runs other scripts (make sure you put ./scripts infront the name)
## Features

- Remotely Edit Payloads
- WiFi Enabled
- Undetectable by Windows, Mac and Linux
- Easily Modifiable

## Authors

- [@bonsall2004](https://www.github.com/bonsall2004)


## Feedback

If you have any feedback, please make a [Github Issue](https://github.com/bonsall2004/PicoDucky/issues) and I'll look into it.


## Acknowledgements

 - [Dbisu's duckyinpython.py (with modifications)](https://github.com/dbisu/)

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

