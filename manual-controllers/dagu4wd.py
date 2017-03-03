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
import bluetoothinput as bt

# Record or record video?
record_video = False

if record_video:
    print "Initialising video"
    import picamera
    import datetime
    d = datetime.datetime.now()
    filename = "media/{}-{}-{}_{}-{}.h264".format(d.year, d.month, d.day, d.hour, d.minute)
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)
    camera.framerate = 30
    camera.start_recording(filename)

# Initialise wild thumper control
print "Initialising control algorithm"
wt4 = WildThumper(4, 7.4, 7, 0)

# Initialise bluetooth controller
print "Initialising bluetooth controller"
joystick = bt.BluetoothInput()

# Initialise loop
stop_loop = False

# Start time
t0 = time.time()

try:
    print "Running controller"

    # Loop
    while joystick != 0 and stop_loop == False:
        buttons, axes, hats = joystick.get_controls()

        # Update motors
        wt4.update_motors(axes['L vertical'], axes['L horizontal'])

        # Update servos
        wt4.update_servos(axes['R vertical'], buttons['R1'])

        # Stop loop if "X" button is pressed
        if buttons['X'] == True:
            stop_loop = True

    print "Controller terminated"

    # Stop motors
    wt4.stop_motors()

    # GPIO cleanup
    wt4.cleanup()

finally:
    # Finish time
    tf = time.time() - t0
    print "Operational time: {:0.3f}s".format(tf)

    # Stop camera
    if record_video:
        camera.stop_recording()
