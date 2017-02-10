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
import RPi.GPIO as GPIO
import numpy as np

# Initialise bluetooth controller
joystick = btcontrol.Init()

# Power settings
MotorVoltage = 7.2
BatteryVoltage = 7.4

# Motor delay to avoid bad things
MotorDelay = 0.2

# Pin allocation
RIGHT_PWM_PIN = 14
LEFT_PWM_PIN = 24
LEFT_1_PIN = 17
LEFT_2_PIN = 4
RIGHT_1_PIN = 10
RIGHT_2_PIN = 25
LED_1_PIN = 8
LED_2_PIN = 7

# Initialise GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_PWM_PIN, GPIO.OUT)
GPIO.setup(LEFT_1_PIN, GPIO.OUT)
GPIO.setup(LEFT_2_PIN, GPIO.OUT)
GPIO.setup(RIGHT_PWM_PIN, GPIO.OUT)
GPIO.setup(RIGHT_1_PIN, GPIO.OUT)
GPIO.setup(RIGHT_2_PIN, GPIO.OUT)
GPIO.setup(LED_1_PIN, GPIO.OUT)
GPIO.setup(LED_2_PIN, GPIO.OUT)

# Set initial values
GPIO.output(LEFT_1_PIN, 0)
GPIO.output(LEFT_2_PIN, 1)
GPIO.output(RIGHT_1_PIN, 0)
GPIO.output(RIGHT_2_PIN, 1)
GPIO.output(LED_1_PIN, 1)
GPIO.output(LED_2_PIN, 1)

# Initialise PWMs
LeftPWM = GPIO.PWM(LEFT_PWM_PIN, 500)
RightPWM = GPIO.PWM(RIGHT_PWM_PIN, 500)
LeftPWM.start(0)
RightPWM.start(0)

# Initialise directions
OldLDir = 1
OldRDir = 1

# Set motor PWMs and direction from joystick commands
def JS2Motor(Vert, Hor, Turbo, OldLDir, OldRDir):
    # Set motor speeds in range [-1 1]
    if Turbo == 1:
        LSpeed = 1
        RSpeed = 1
    else:
        LSpeed = -0.8*Vert + 0.8*Hor
        RSpeed = -0.8*Vert - 0.8*Hor

    # Set motor directions
    if LSpeed > 1:
        LSpeed = 1
        LDir = 1
    elif LSpeed >= 0:
        LDir = 1
    elif LSpeed < -1:
        LSpeed = -1
        LDir = -1
    else:
        LDir = -1
    
    if RSpeed > 1:
        RSpeed = 1
        RDir = 1
    elif RSpeed >= 0:
        RDir = 1
    elif RSpeed < -1:
        RSpeed = -1
        RDir = -1
    else:
        RDir = -1
    
    # If motors cmds have changed direction, stop them briefly
    if OldLDir != LDir or OldRDir != RDir:

        GPIO.output(LEFT_1_PIN, OldLDir != 1)
        GPIO.output(LEFT_2_PIN, OldLDir == 1)
        GPIO.output(RIGHT_1_PIN, OldRDir != 1)
        GPIO.output(RIGHT_2_PIN, OldRDir == 1)
    
        # Set motor speeds to zero
        LeftPWM.ChangeDutyCycle(0)
        RightPWM.ChangeDutyCycle(0)
        time.sleep(MotorDelay)

    else:
        
        GPIO.output(LEFT_1_PIN, LDir != 1)
        GPIO.output(LEFT_2_PIN, LDir == 1)
        GPIO.output(RIGHT_1_PIN, RDir != 1)
        GPIO.output(RIGHT_2_PIN, RDir == 1)
    
        # Set motor PWMs based on speeds and power ratio
        scale = MotorVoltage/BatteryVoltage
        LeftPWM.ChangeDutyCycle(LDir*LSpeed*100*scale)
        RightPWM.ChangeDutyCycle(RDir*RSpeed*100*scale)

    # Save directions for next loop
    return LDir, RDir

# Print variable
PrintStuff = False

# Initialise loop
StopLoop = False

# Loop
while joystick != 0 and StopLoop == False:
    buttons, axes = btcontrol.GetControls( joystick )

    OldLDir, OldRDir = JS2Motor(axes['L vertical'], axes['L horizontal'], buttons['R2'], OldLDir, OldRDir)

    # Stop loop if "X" button is pressed
    if buttons['X'] == True:
        print("Stopping rover")
        StopLoop = True

# Stop PWMs
LeftPWM.stop()
RightPWM.stop()

# Turn off LEDs
GPIO.output(LED_1_PIN, 0)
GPIO.output(LED_2_PIN, 0)

# Release pins and clean up
GPIO.cleanup()