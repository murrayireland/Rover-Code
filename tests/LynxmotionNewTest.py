# Test of new Lynxmotion controller with Adafruit DC
# motor driver and Sense HAT IMU

import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
