#!/usr/bin/env python

"""
DCDriverTest.py: Test of Cytron DC motor driver and Adafruit PWM
driver. This code is derived from the examples supplied by
Adafruit.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "24/01/17"

import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO

# Set max and min pulse lengths (out of 4096)
pulse_min = 2000
pulse_max = 4096

# Set channel
channel = 15

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Disable warnings
GPIO.setwarnings(False)

# Pin for direction control
dir_pin = 22

# Set pins as outputs
GPIO.setup(dir_pin, GPIO.OUT)

# Set direction 
GPIO.output(dir_pin, GPIO.HIGH)

# Initialise PWM driver
pwm = Adafruit_PCA9685.PCA9685()

# Set PWM frequency to 20 Hz
pwm.set_pwm_freq(500)

while True:
    # Move servo between extremes
    pwm.set_pwm(channel, 0, pulse_min)
    time.sleep(1)
    pwm.set_pwm(channel, 0, pulse_max)
    time.sleep(1)

# Clean up GPIO
GPIO.cleanup()