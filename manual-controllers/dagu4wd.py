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
from sense_hat import SenseHat

# Record or record video?
record_video = False

# Record data?
record_data = True

if record_video or record_data:
    import os
    import datetime
    d = datetime.datetime.now()
    if os.path.isdir("./dagu4wd_data") == False:
        os.mkdir("dagu4wd_data")

if record_video:
    print "Initialising video"
    import picamera
    vidname = "dagu4wd_data/video_{}-{}-{}_{}-{}.h264".format(d.year, d.month, d.day, d.hour, d.minute)
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)
    camera.framerate = 30
    camera.start_recording(vidname)

if record_data:
    print "Initialising black box"
    import csv
    import numpy as np
    import io
    bbname = "dagu4wd_data/blackbox_{}-{}-{}_{}-{}.txt".format(d.year, d.month, d.day, d.hour, d.minute)

# Initialise wild thumper control
print "Initialising control algorithm"
wt4 = WildThumper(4, 7.4, 7, 0)

# Initialise bluetooth controller
print "Initialising bluetooth controller"
joystick = bt.BluetoothInput()

# Initialise sensors
sense = SenseHat()
sense.set_rotation(90)
e = (0, 0, 0)
white = (255, 255, 255)

# LED set function
def set_LEDs(coords):
    # Blank LEDs
    clrs = [
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e
    ]

    # Set coords to white
    for coord in coords:
        clrs[coord[0] + 8*coord[1]] = white

    # Update Sense HAT
    sense.set_pixels(clrs)

# Initialise loop
stop_loop = False

# Start time
T0 = time.time()
t = 0

try:
    print "Running controller"

    # Loop
    while joystick != 0 and stop_loop == False:
        # Get controls
        buttons, axes, hats = joystick.get_controls()

        # Visualise controls on LED matrix
        led_x = int( round( 3*axes['L horizontal'] + 3 ) )
        led_y = int( round( 3*axes['L vertical'] + 3 ) )
        coords = ( (led_x, led_y), (led_x+1, led_y), (led_x, led_y+1), (led_x+1, led_y+1) )
        set_LEDs( coords )

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
    tf = time.time() - T0
    print "Operational time: {:0.3f}s".format(tf)

    # Stop camera
    if record_video:
        camera.stop_recording()
