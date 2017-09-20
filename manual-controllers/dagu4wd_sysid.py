#!/usr/bin/env python

"""
dagu4wd.py: Manual controller for Dagu Wild Thumper 4WD. Bluetooth
controller is used to provide remote control of rover.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "24/01/17"

import time
#from sense_hat import SenseHat
import Adafruit_PCA9685 as PD
import RPi.GPIO as GPIO
from numpy import sign

# Select test
# 1 - forward
# 2 - reverse
# 3 - clockwise
# 4 - counter-clockwise
test = 1

# Record data?
record_data = False

if record_data:
    print "Initialising black box"
    import csv
    import numpy as np
    import io
    import os
    import datetime
    d = datetime.datetime.now()
    if os.path.isdir("./dagu4wd_data") == False:
        os.mkdir("dagu4wd_data")
    bbname = "dagu4wd_data/blackbox_{}-{}-{}_{}-{}.txt".format(d.year, d.month, d.day, d.hour, d.minute)

    # Settings
    Data_Time = np.zeros(1)
    Data_Inputs = np.zeros((4,1))
    Data_Outputs = np.zeros((9,1))

# Initialise controller
GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False ) 
motor_pins = {'BL': 17, 'BR': 18, 'FL': 6, 'FR': 12}
motor_chls = {'BL': 0, 'BR': 1, 'FL': 14, 'FR': 15}
motor_dirs = {'BL': -1, 'BR': 1, 'FL': -1, 'FR': 1}

for motor in motor_pins:
    GPIO.setup( motor_pins[motor], GPIO.OUT )

speed = 0.4

if test == 1:
    test_cmds = {'BL': speed, 'BR': speed, 'FL': speed, 'FR': speed}
    test_dirs = {'BL': 0, 'BR': 1, 'FL': 0, 'FR': 1}
    test_pols = {'BL': 1, 'BR': 1, 'FL': 1, 'FR': 1}
elif test == 2:
    test_cmds = {'BL': speed, 'BR': speed, 'FL': speed, 'FR': speed}
    test_dirs = {'BL': 1, 'BR': 0, 'FL': 1, 'FR': 0}
    test_pols = {'BL': -1, 'BR': -1, 'FL': -1, 'FR': -1}
elif test == 3:
    test_cmds = {'BL': speed, 'BR': speed, 'FL': speed, 'FR': speed}
    test_dirs = {'BL': 0, 'BR': 0, 'FL': 0, 'FR': 0}
    test_pols = {'BL': 1, 'BR': -1, 'FL': 1, 'FR': -1}
elif test == 4:
    test_cmds = {'BL': speed, 'BR': speed, 'FL': speed, 'FR': speed}
    test_dirs = {'BL': 1, 'BR': 1, 'FL': 1, 'FR': 1}
    test_pols = {'BL': -1, 'BR': 1, 'FL': -1, 'FR': 1}
elif test == 5:
    test_cmds = {'BL': 0, 'BR': 0, 'FL': 0, 'FR': 0}
    test_dirs = {'BL': 1, 'BR': 1, 'FL': 1, 'FR': 1}
    test_pols = {'BL': -1, 'BR': 1, 'FL': -1, 'FR': 1}

motor_voltage = 7
battery_voltage = 7.4
pwm_scale = motor_voltage / battery_voltage
bit_length = 4095

motors = PD.PCA9685()
motors.set_pwm_freq(50)

voltages = {'BL': 0., 'BR': 0., 'FL': 0., 'FR': 0.}

# Initialise sensors
#sense = SenseHat()
#sense.set_rotation(90)

# Sensor data
#def retrieve_sensor_data():
    # Accelerometers
    #acc = sense.get_accelerometer_raw()

    # Gyroscopes
    #gyro = sense.get_gyroscope_raw()

    # Magnetometers
    #mag = sense.get_compass_raw()

    # Return results
    #return (acc['x'], acc['y'], acc['z'], gyro['x'], gyro['y'], gyro['z'], mag['x'], mag['y'], mag['z'])

# Start time
T0 = time.time()
t = 0.
tf = 4
dt_samp = 0.01
t_samp = 0.

print "Running experiment"

while t <= tf:

    # Tests
    for motor in motor_chls:
        if t < 0:
            voltages[motor] = 0
            dc = 0
        else:
            voltages[motor] = test_cmds[motor] * test_pols[motor] * motor_voltage
            dc = int( test_cmds[motor]*pwm_scale*bit_length )
        GPIO.output( motor_pins[motor], test_dirs[motor] )
        motors.set_pwm( motor_chls[motor], 0, dc )

    t = time.time() - T0

    if t >= t_samp and record_data:

        # Retrieve inputs
        inputs = ( voltages['BL'], voltages['BR'], voltages['FL'], voltages['FR'] )
        inputs_save = []
        inputs_save.append( inputs )
        inputs_save = np.transpose( [[x for xs in inputs_save for x in xs]] )

        # Retreive sensor data
        outputs = retrieve_sensor_data()
        outputs_save = []
        outputs_save.append( outputs )
        outputs_save = np.transpose( [[x for xs in outputs_save for x in xs]] )

        Data_Time = np.concatenate( ( Data_Time, [t] ), axis=1 )
        Data_Inputs = np.concatenate( ( Data_Inputs, inputs_save ), axis=1 )
        Data_Outputs = np.concatenate( ( Data_Outputs, outputs_save ), axis=1 )

        t_samp = t_samp + dt_samp

print "Stopping"

for motor in motor_chls:
    motors.set_pwm( motor_chls[motor], 0, 0 )

# Save data
if record_data:
	print "Saving data"
	with io.FileIO( bbname, "w" ) as file:
	    writeobject = csv.writer( file, delimiter="\t" )
	    writeobject.writerow( Data_Time )
	    for row in Data_Inputs:
	        writeobject.writerow( row )
	    for row in Data_Outputs:
        	writeobject.writerow( row )

# End
