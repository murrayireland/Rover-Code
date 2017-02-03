#!/usr/bin/env python

"""
Help.py: Turns stuff off.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "24/01/17"

import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Disable warnings
GPIO.setwarnings(False)

# Pins to turn off
Pins = [17, 18, 22, 23]

for Pin in Pins:
    GPIO.setup(Pin, GPIO.OUT)
    GPIO.output(Pin, GPIO.LOW)

GPIO.cleanup()
