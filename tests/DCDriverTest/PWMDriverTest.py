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
dir_pin = 18

# Pin for PWM control
pwm_pin = 14

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

for speed in range(0, 100, 10):
    print "Speed: {}".format(speed)
    set_pwm_dc(pwm_pin, 0, speed)
    time.sleep(1)

# Clean up GPIO
GPIO.cleanup()
