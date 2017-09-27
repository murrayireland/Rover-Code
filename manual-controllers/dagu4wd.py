#!/usr/bin/env python

"""
dagu4wd.py: Manual controller for Dagu Wild Thumper 4WD. Bluetooth
controller is used to provide remote control of rover.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "21/09/17"

import time
from wildthumper import WildThumper
import bluetoothinput as bt
from sense_hat import SenseHat

# Allow turbo mode?
Turbo = True

# Record or record video?
record_video = False

# Record data?
record_data = True
print_data = False

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

    # Black box settings
    dt_samp = 0.1
    t_samp = 0
    Data_Time = np.zeros(1)
    Data_Inputs = np.zeros((4,1))
    Data_Outputs = np.zeros((9,1))

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

# Sensor data
def retrieve_sensor_data():
    # Accelerometers
    acc = sense.get_accelerometer_raw()

    # Gyroscopes
    gyro = sense.get_gyroscope_raw()

    # Magnetometers
    mag = sense.get_compass_raw()

    # Return results
    return (acc, gyro, mag)

# Controller settings
Kcoll = -0.6
Kdiff = 0.3

# Initialise loop
stop_loop = False

# Start time
T0 = time.time()
t = 0

try:
    print "Running controller"

    # Loop
    while joystick != 0 and stop_loop == False:
        # Get joystick controls
        buttons, axes, hats = joystick.get_controls()

        # Get vehicle controls
        if buttons['R1'] == True and buttons['L1'] == True and Turbo == True:
            coll = 1
            diff = 0
        elif buttons['R1'] == True and Turbo == True:
            coll = 0
            diff = 1
        elif buttons['L1'] == True and Turbo == True:
            coll = 0
            diff = -1
        else:
            coll = Kcoll*axes['L vertical']
            diff = Kdiff*axes['L horizontal']

        # Visualise controls on LED matrix
        led_x = int( round( 3*diff + 3 ) )
        led_y = int( round( 3*coll + 3 ) )
        coords = ( (led_x, led_y), (led_x+1, led_y), (led_x, led_y+1), (led_x+1, led_y+1) )
        set_LEDs( coords )

        # Update motors
        voltages = wt4.update_motors(coll, diff)

        # Update servos
        wt4.update_servos(axes['R vertical'], buttons['R stick'])

        # Save data to arrays
        t = time.time() - T0
        if record_data:
            if t >= t_samp:

                # Save time
                Data_Time = np.concatenate( ( Data_Time, [t] ), axis=1 )

                # Save inputs
                inputs = np.array( [[voltages['BL']],
                                    [voltages['FL']],
                                    [voltages['FR']],
                                    [voltages['BR']]] )
                Data_Inputs = np.concatenate( ( Data_Inputs, inputs ), axis=1 )

                # Save outputs
                acc, gyro, mag = retrieve_sensor_data()
                outputs = np.array( [[acc['x']],
                                     [acc['y']],
                                     [acc['z']],
                                     [gyro['x']],
                                     [gyro['y']],
                                     [gyro['z']],
                                     [mag['x']],
                                     [mag['y']],
                                     [mag['z']]] )
                Data_Outputs = np.concatenate( ( Data_Outputs, outputs ), axis=1 )

                # Increment sample time
                t_samp = t_samp + dt_samp
                
                if print_data:
                    print "Time {:0.3f} s, Inputs = ({:0.3f}, {:0.3f}, {:0.3f}, {:0.3f})".format( t, float(inputs[0]), float(inputs[1]), float(inputs[2]), float(inputs[2]) )

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
