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
DC_min = 25
DC_max = 50

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Disable warnings
GPIO.setwarnings(False)

motor = 'FR'

# Direction pins
motor_pins_6wd = {'BL': 17, 'ML': 22, 'FL': 6,
                  'BR': 18, 'MR': 27, 'FR': 12}

# PWM channels
motor_chls_6wd = {'BL': 14, 'ML': 1, 'FL': 8,
                  'BR': 15, 'MR': 0, 'FR': 9}

# Motor polarity
motor_pols_6wd = {'BL': 1, 'ML': 1, 'FL': 1,
                  'BR': 0, 'MR': 0, 'FR': 0}

# GPIO pin for direction control
dir_pin = motor_pins_6wd[motor]

# PWM controller channel
pwm_pin = motor_chls_6wd[motor]

# Set pins as outputs
GPIO.setup(dir_pin, GPIO.OUT)

# Set direction
# GPIO.output(dir_pin, GPIO.LOW)
GPIO.output(dir_pin, motor_pols_6wd[motor])

# Initialise PWM driver
pwm = Adafruit_PCA9685.PCA9685()

# Set PWM frequency (Hz)
pwm.set_pwm_freq(200)

# Set PWM from duty cycle
def set_pwm_dc(channel, on_dc, off_dc):
    # Scale on/off parameters
    on_bits = int(round((on_dc/100.0)*4095))
    off_bits = int(round((off_dc/100.0)*4095))

    # Set PWM for channel
    pwm.set_pwm(channel, on_bits, off_bits)

set_pwm_dc(pwm_pin, 0, 20)
time.sleep(2)

set_pwm_dc(pwm_pin, 0, 0)
time.sleep(1)

GPIO.output(dir_pin, not(motor_pols_6wd[motor]))

set_pwm_dc(pwm_pin, 0, 20)
time.sleep(2)

set_pwm_dc(pwm_pin, 0, 0)
time.sleep(1)

# Clean up GPIO
GPIO.cleanup()
