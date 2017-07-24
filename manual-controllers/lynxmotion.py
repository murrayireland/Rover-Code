#!/usr/bin/env python

"""
Lynxmotion.py: Manual control module for Lynxmotion 4WD3 rover.
Bluetooth gamepad is used for input and RasPiRobot board v3
provides interface with motors.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "20/01/17"

import time
from adafruitDriver import AdafruitDriver
import bluetoothinput as bt
from sense_hat import SenseHat

# Record  video?
record_video = True

if record_video:
    print "Initialising video"
    import picamera
    import datetime
    import os
    d = datetime.datetime.now()
    print os.path.isdir("./media")
    if os.path.isdir("./media") == False:
        os.mkdir("media")
    filename = "media/{}-{}-{}_{}-{}.h264".format(d.year, d.month, d.day, d.hour, d.minute)
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)
    camera.framerate = 30
    camera.start_recording(filename)

# Initialise controller
print "Initialising control algorithm"
controller = AdafruitDriver(7.4, 7.2, 1)

# Initialise bluetooth controller
print "Initialising bluetooth controller"
joystick = bt.BluetoothInput()

# Initialise sensors
sense = SenseHat()
sense.set_rotation(270)

e = (0, 0, 0)
white = (255, 255, 255)

# LED set function
def set_LEDs(coords, ):
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

# Black box settings
dt_samp = 0.1
Data_Inputs = np.zeros((2,1))
Data_Outputs = np.zeros((9,1))

# Initialise loop
stop_loop = False

# Start time
T0 = time.time()

try:
    print "Running controller"

    # Loop
    while joystick != 0 and stop_loop == False:
        buttons, axes, hats = joystick.get_controls()

        # Visualise controls
        led_x = int(round(3*axes['L horizontal'] + 3))
        led_y = int(round(3*axes['L vertical'] + 3))
        set_LEDs( (led_x, led_y), (led_x+1, led_y), (led_x, led_y+1), (led_x+1, led_y+1) )

        # Update motors
        controller.update_motors(axes['L vertical'], axes['L horizontal'])

        # Stop loop if "X" button is pressed
        if buttons['X'] == True:
            stop_loop = True

    print "Controller terminated"

    # GPIO cleanup
    controller.cleanup()

finally:
    # Finish time
    tf = time.time() - t0
    print "Operational time: {:0.3f}s".format(tf)

    # Stop camera
    if record_video:
        camera.stop_recording()
