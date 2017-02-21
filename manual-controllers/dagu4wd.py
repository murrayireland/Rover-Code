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

# Record or record video?
record_video = "record"

if record_video == "record":
    import picamera
    import datetime
    d = datetime.datetime.now()
    filename = "~/git/Rover-Code/media/{}-{}-{}_{}-{}.h264".format(d.year, d.month, d.day, d.hour, d.minute)
    camera = picamera.PiCamera()
    camera.resolution = (1200, 800)
    camera.start_recording(filename)

elif record_video == "stream":
    import picamera
    import socket
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 5

    # Server setup
    server_socket = socket.socket()
    # server_socket.close()
    server_socket.bind(("0.0.0.0", 8000))
    server_socket.listen(0)

    # Accept a single connection and make a file out of it
    print "Please connect to video stream"
    connection = server_socket.accept()[0].makefile('wb')
    camera.start_recording(connection, format="h264")

# Initialise wild thumper control
wt4 = WildThumper(4, 7.4, 7, 0)

# Initialise bluetooth controller
joystick = btcontrol.Init()

# Initialise loop
stop_loop = False

# Start time
t0 = time.time()

print "Running controller"

# Loop
while joystick != 0 and stop_loop == False:
    buttons, axes = btcontrol.GetControls(joystick)

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

# Finish time
tf = time.time() - t0
print "Operational time: {:0.3f}s".format(tf)

# Stop camera
if record_video == "record":
    camera.stop_recording()
elif record_video == "stream":
    camera.stop_recording()
    connection.close()
    server_socket.close()
