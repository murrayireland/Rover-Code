# Calibrate controller signals and write for use elsewhere
# Murray Ireland
# 05/01/2017
__author__ = 'Murray Ireland'

import BluetoothController, time
import RPi.GPIO as GPIO

# Initialise bluetooth controller
joystick = BluetoothController.Init()

# Initialise PWM
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm = GPIO.PWM(11, 50)
pwm.start(5)

# Print variable
PrintStuff = False

# Initialise loop
StopLoop = False

# Loop
while joystick != 0 and StopLoop == False:
    buttons, axes = BluetoothController.GetControls( joystick )

    # Print buttons if active
    if PrintStuff == True and any(b > 0 for b in buttons.itervalues()):
        print buttons
    
    # Print axes if active
    if PrintStuff == True and any(abs(a) > 0 for a in axes.itervalues()):
        print axes

    # Scale controls for duty cycle
    DC = 2.5*axes['L vertical'] + 7.5

    print DC
    
    # Write controls to servo
    pwm.ChangeDutyCycle(DC)

    # Stop loop if "X" button is pressed
    if buttons['X'] == True:
        StopLoop = True

# Stop PWM
pwm.stop()

# Release pins and clean up
GPIO.cleanup()