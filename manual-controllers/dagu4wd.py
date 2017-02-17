#!/usr/bin/env python

"""
dagu4wd.py: Manual controller for Dagu Wild Thumper 4WD. Bluetooth
controller is used to provide remote control of rover.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "24/01/17"

import time
from wildthumper import WildThumper
import btcontrol

# Initialise wild thumper control
wt4 = WildThumper(4, 7.4, 5, 0)

# Initialise bluetooth controller
joystick = btcontrol.Init()

# Initialise loop
stop_loop = False

# Loop
while joystick != 0 and stop_loop == False:
    buttons, axes = btcontrol.GetControls(joystick)

    # Update motors
    wt4.update_motors(axes['L vertical'], axes['L horizontal'])

    # Stop loop if "X" button is pressed
    if buttons['X'] == True:
        stop_loop = True

# Stop motors
wt4.stop_motors()

# GPIO cleanup
wt4.cleanup()
