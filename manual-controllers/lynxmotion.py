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

# Record data?
record_data = True
print_data = True

if record_video or record_data:
    import os
    import datetime
    d = datetime.datetime.now()
    if os.path.isdir("./lynxmotion_data") == False:
        os.mkdir("lynxmotion_data")


if record_video:
    print "Initialising video"
    import picamera
    vidname = "lynxmotion_data/video_{}-{}-{}_{}-{}.h264".format(d.year, d.month, d.day, d.hour, d.minute)
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)
    camera.framerate = 30
    camera.start_recording(vidname)

if record_data:
    print "Initialising black box"
    import csv
    import numpy as np
    import io
    bbname = "lynxmotion_data/blackbox_{}-{}-{}_{}-{}.txt".format(d.year, d.month, d.day, d.hour, d.minute)

    # Black box settings
    dt_samp = 0.1
    t_samp = 0
    Data_Time = np.zeros(1)
    Data_Inputs = np.zeros((2,1))
    Data_Outputs = np.zeros((9,1))

# Initialise controller
print "Initialising control algorithm"
controller = AdafruitDriver(7.4, 7.2, "Lynxmotion", 0)

# Initialise bluetooth controller
print "Initialising bluetooth controller"
joystick = bt.BluetoothInput()

# Initialise sensors
sense = SenseHat()
sense.set_rotation(270)

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

# Sensor data
def retrieve_sensor_data():
    # Accelerometers
    acc = sense.get_accelerometer_raw()

    # Gyroscopes
    gyro = sense.get_gyroscope_raw()

    # Magnetometers
    mag = sense.get_compass_raw()

    # Return results
    return (acc['x'], acc['y'], acc['z'], gyro['x'], gyro['y'], gyro['z'], mag['x'], mag['y'], mag['z'])

# Initialise loop
stop_loop = False

# Start time
T0 = time.time()
t = 0

try:
    print "Running controller"

    # Loop
    while joystick != 0 and stop_loop == False:
        buttons, axes, hats = joystick.get_controls()

        # Visualise controls
        led_x = int(round(3*axes['L horizontal'] + 3))
        led_y = int(round(3*axes['L vertical'] + 3))
        coords = ( (led_x, led_y), (led_x+1, led_y), (led_x, led_y+1), (led_x+1, led_y+1) )
        set_LEDs( coords )

        # Update motors
        inputs = controller.update_motors(axes['L vertical'], axes['L horizontal'])
        inputs_save = []
        inputs_save.append( inputs )
        inputs_save = np.transpose( [[x for xs in inputs_save for x in xs]] )

        # Retreive sensor data
        outputs = retrieve_sensor_data()
        outputs_save = []
        outputs_save.append( outputs )
        outputs_save = np.transpose( [[x for xs in outputs_save for x in xs]] )

        # Save data to arrays
        t = time.time() - T0
        if record_data:
            if t >= t_samp:
                Data_Time = np.concatenate( ( Data_Time, [t] ), axis=1 )
                Data_Inputs = np.concatenate( ( Data_Inputs, inputs_save ), axis=1 )
                Data_Outputs = np.concatenate( ( Data_Outputs, outputs_save ), axis=1 )
                t_samp = t_samp + dt_samp
                
                if print_data:
                    print "Time {:0.3f} s, Inputs = ({:0.3f}, {:0.3f}), Acc = ({:0.3f}, {:0.3f}, {:0.3f})".format(t, inputs[0], inputs[1], outputs[0], outputs[1], outputs[2])


        # Stop loop if "X" button is pressed
        if buttons['X'] == True:
            stop_loop = True

    print "Controller terminated"

    # GPIO cleanup
    controller.cleanup()

finally:
    # Finish time
    tfin = time.time() - T0
    print "Operational time: {:0.3f}s".format(tfin)

    # Stop camera
    if record_video:
        print "Stopping camera"
        camera.stop_recording()

    # Save data
    if record_data:
        print "Saving data"
        with io.FileIO( bbname, "w" ) as file:
            writeobject = csv.writer( file, delimiter='\t' )
            writeobject.writerow( Data_Time )
            for row in Data_Inputs:
                writeobject.writerow( row )
            for row in Data_Outputs:
                writeobject.writerow( row )

# End
