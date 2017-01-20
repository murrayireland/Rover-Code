#!/usr/bin/env python

"""
Lynxmotion.py: Manual control module for Lynxmotion 4WD3 rover.
Bluetooth gamepad is used for input and RasPiRobot board v3
provides interface with motors.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "20/01/17"

import btcontrol
import time
from rrb3 import *
import numpy as np

# Initialise bluetooth controller
joystick = btcontrol.Init()

# Initialise RasPiRobot board
rr = RRB3(7.4, 7.2)

# Turn on LEDs
rr.set_led1(1)
rr.set_led2(1)

# Print variable
PrintStuff = False

# Initialise loop
StopLoop = False

# Loop
while joystick != 0 and StopLoop == False:
    buttons, axes = btcontrol.GetControls( joystick )

    # Print buttons if active
    if PrintStuff == True and any(b > 0 for b in buttons.itervalues()):
        print buttons
    
    # Print axes if active
    if PrintStuff == True and any(abs(a) > 0 for a in axes.itervalues()):
        print axes

    # Get motor speeds and directions
    Coll = -1*axes['L vertical']
    Diff = 1*axes['L horizontal']
    Speed = [0.5*Coll+1*Diff, 0.5*Coll-1*Diff]
    # if Speed[0] != 0 or Speed[1] != 0:
    #     print Diff
    
    Dir = [0, 0]
    for i in range(0, 2):
        if Speed[i] > 1:
            Speed[i] = 1
        elif Speed[i] < -1:
            Speed[i] = -1
        if Speed[i] < 0:
            Dir[i] = 1
    Speed = np.absolute(Speed)

    # Override with turbo
    if buttons['R2'] == True:
        Speed = [1, 1]
        Dir = [0, 0]
    elif buttons['L2'] == True:
        Speed = [1, 1]
        Dir = [1, 1]    
    
    #print( Speed )
    #print( Dir )
    #time.sleep(0.5)

    # Write motor speeds and directions
    rr.set_motors(Speed[0],Dir[0],Speed[1],Dir[1])

    # Stop loop if "X" button is pressed
    if buttons['X'] == True:
        StopLoop = True

# Turn on LEDs
rr.set_led1(0)
rr.set_led2(0)

# Clean up
rr.cleanup()