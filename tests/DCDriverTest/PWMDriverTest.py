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

# Set max and min duty cycles
DC_min = 1
DC_max = 100

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Disable warnings
GPIO.setwarnings(False)

# Pin for direction control
dir_pin = 17

# Set pins as outputs
GPIO.setup(dir_pin, GPIO.OUT)

# Set direction
GPIO.output(dir_pin, GPIO.HIGH)

# Initialise PWM driver
pwm = Adafruit_PCA9685.PCA9685()

# Set PWM frequency (Hz)
pwm.set_pwm_freq(50)

# Set PWM from duty cycle
def set_pwm_dc(channel, on_dc, off_dc):
    # Scale on/off parameters
    on_bits = int(round((on_dc/100.0)*4095))
    off_bits = int(round((off_dc/100.0)*4095))

    # Set PWM for channel
    pwm.set_pwm(channel, on_bits, off_bits)

count = 0
while count < 3:
    set_pwm_dc(0, 0, DC_min)
    time.sleep(1)
    set_pwm_dc(0, 0, DC_max)
    time.sleep(1)
    count = count + 1

pwm.set_pwm(0, 0, 0)
time.sleep(1)

# Clean up GPIO
GPIO.cleanup()
