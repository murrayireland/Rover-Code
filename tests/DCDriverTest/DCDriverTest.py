#!/usr/bin/env python

"""
DCDriverTest.py: Test of Cytron DC motor driver, with PWM signals
supplied directly by Raspberry Pi. This code is derived from the
MDD10A.py module created by Mohammad Omar
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "24/01/17"

# Import libraries
import time
import RPi.GPIO as GPIO

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Disable warnings
GPIO.setwarnings(False)

# Constants
pwm_max = 100

# Pins for Raspberry Pi 3
l_dir_pin = 22
r_dir_pin = 23
l_pwm_pin = 17
r_pwm_pin = 18

# Set up directions
GPIO.setup(l_dir_pin, GPIO.OUT)
GPIO.setup(r_dir_pin, GPIO.OUT)

# Set direction pin values to low
GPIO.output(l_dir_pin, GPIO.LOW)
GPIO.output(r_dir_pin, GPIO.LOW)

# Set up speeds
GPIO.setup(l_pwm_pin, GPIO.OUT)
GPIO.setup(r_pwm_pin, GPIO.OUT)

# Set motor pin frequency to 20 Hz
l_pwm = GPIO.PWM(l_pwm_pin, 20)
r_pwm = GPIO.PWM(r_pwm_pin, 20)

# Start PWM channels and set duty cycle
l_pwm.start(0)
l_pwm.ChangeDutyCycle(0)
r_pwm.start(0)
r_pwm.ChangeDutyCycle(0)

for i in range(0, 100, 1):
    # Change duty cycle
    l_pwm.ChangeDutyCycle(i)
    r_pwm.ChangeDutyCycle(i)

    # Wait
    time.sleep(0.2)

# Stop
l_pwm.stop()
r_pwm.stop()

# Clean up
GPIO.cleanup()