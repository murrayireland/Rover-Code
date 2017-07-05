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
import Adafruit_PCA9685 as PD

# Set max and min duty cycles
DC_min = 4.5
DC_max = 7.2

# PWM controller channel
pwm_pin = 5

# Initialise PWM driver
pwm = PD.PCA9685()
pwm.set_pwm_freq(50)

# Set PWM from duty cycle
def set_pwm_dc(channel, on_dc, off_dc):
    # Scale on/off parameters
    on_bits = int(round((on_dc/100.0)*4095))
    off_bits = int(round((off_dc/100.0)*4095))

    # Set PWM for channel
    pwm.set_pwm(channel, on_bits, off_bits)

# time.sleep(2)

set_pwm_dc(pwm_pin, 0, DC_min)
time.sleep(1)

set_pwm_dc(pwm_pin, 0, DC_max)
time.sleep(1)

#for speed in range(0, 200, 10):
#    print "DC: {}".format(speed/10.0)
 #   set_pwm_dc(pwm_pin, 0, speed/10.0)
  #  time.sleep(1)

set_pwm_dc(pwm_pin, 0, DC_min)
