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
record_video = False

if record_video:
    print "Initialising video"
    import picamera
    import datetime
    import os
    d = datetime.datetime.now()
    if os.path.isdir("/media") == False:
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
blnk = [
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e
]

# Initialise loop
stop_loop = False

# Start time
t0 = time.time()

try:
    print "Running controller"

    # Loop
    while joystick != 0 and stop_loop == False:
        buttons, axes, hats = joystick.get_controls()

        # Visualise controls
        led_x = int(round(3*axes['L horizontal'] + 3))
        led_y = int(round(3*axes['L vertical'] + 3))
        sense.set_pixels(blnk)
        sense.set_pixel(led_x, led_y, (255, 255, 255))
        sense.set_pixel(led_x+1, led_y, (255, 255, 255))
        sense.set_pixel(led_x, led_y+1, (255, 255, 255))
        sense.set_pixel(led_x+1, led_y+1, (255, 255, 255))

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
