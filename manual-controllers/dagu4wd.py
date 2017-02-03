#!/usr/bin/env python

"""
dagu4wd.py: Manual controller for Dagu Wild Thumper 4WD. Bluetooth
controller is used to provide remote control of rover.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "24/01/17"

import time
import Adafruit_PCA9685 as PD
import RPi.GPIO as GPIO
import btcontrol

# Initialise bluetooth controller
Joystick = btcontrol.Init()

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Disable warnings
GPIO.setwarnings(False)

# PWM pins on motor driver board are set to HIGH for locked antiphase
# operation. Pins are allocated as follows
Motor_Pins = {'BL': 18, 'FL': 17, 'BR': 23, 'FR': 22}

# DIR pins on motor driver board are fed PWM signal by PWM controller.
# PWM channels are allocated as follows
Motor_Channels = {'BL': 0, 'FL': 1, 'BR': 14, 'FR': 15}

# Set motor directions
Motor_Dirs = {'BL': -1, 'FL': -1, 'BR': 1, 'FR': 1}

# Servo channels on PWM controller are as follows
Servo_Channels = {'Arm': 4, 'Grasper': 5}

# Set up PWM driver
Motor_Freq = 50
PWM = PD.PCA9685()
PWM.set_pwm_freq(Motor_Freq)

# Set up servos
Servo_Freq = 20
Servo = PD.PCA9685()
Servo.set_pwm_freq(Servo_Freq)

# Get collective and differential speeds from joystick
def Control2Speed(Ver, Hor):
    # Calculate collective and differential components
    Coll = -1*Ver
    Diff = -1*Hor

    # Calculate and return speeds for each side
    Speed = [0.5*Coll-0.5*Diff, 0.5*Coll+0.5*Diff]
    return Speed

# Convert speed in range [-1, 1] to bit rate for PWM driver
def Speed2PWM(Channel, Speed, Dir):
    m = Dir*4095/2.0
    c = 4095/2.0
    Bits = int(round(Speed*m+c))

    # Set PWM for channel
    # print "Channel: {}, PWM: {}".format(Channel, Bits)
    PWM.set_pwm(Channel, 0, Bits)

def Servo2PWM(Channel, Cmd):
    m = 0.15*4095/2.0
    c = 0.225*4095
    Bits = int(round(Cmd*m+c))

    # Set PWM for channel
    Servo.set_pwm(Channel, 0, Bits)

def Button2PWM(Channel, Cmd):
    Off = 0.15*4095
    On = 0.3*4095
    Bits = int(Cmd*(On - Off) + Off)

    # Set PWM for channel 
    print "Cmd: {}".format(Bits)
    Servo.set_pwm(Channel, 0, Bits)

# Set all PWM pins to HIGH for locked antiphase operation
for motor in Motor_Pins:
    GPIO.setup(Motor_Pins[motor], GPIO.OUT)
    GPIO.output(Motor_Pins[motor], GPIO.HIGH)
    Speed2PWM(Motor_Channels[motor], 0, Motor_Dirs[motor])

# Initialise loop
Stop_Loop = False

# Loop
while Joystick != 0 and Stop_Loop == False:
    Buttons, Axes = btcontrol.GetControls(Joystick)

    # Get motor speeds from controls
    Speed = Control2Speed(Axes['L vertical'], Axes['L horizontal'])

    # Send speeds to each motor
    Speed2PWM(Motor_Channels['BL'], Speed[0], Motor_Dirs['BL'])
    Speed2PWM(Motor_Channels['FL'], Speed[0], Motor_Dirs['FL'])
    Speed2PWM(Motor_Channels['BR'], Speed[1], Motor_Dirs['BR'])
    Speed2PWM(Motor_Channels['FR'], Speed[1], Motor_Dirs['FR'])

    # Send commands to each servo 
    Servo2PWM(Servo_Channels['Arm'], Axes['R vertical'])
    Servo2PWM(Servo_Channels['Grasper'], Axes['R horizontal'])

    # Stop loop if "X" button is pressed
    if Buttons['X'] == True:
        Stop_Loop = True

# Stop motors
for motor in Motor_Pins:
    GPIO.output(Motor_Pins[motor], GPIO.LOW)
    PWM.set_pwm(Motor_Channels[motor], 0, 0)

# GPIO cleanup
GPIO.cleanup()