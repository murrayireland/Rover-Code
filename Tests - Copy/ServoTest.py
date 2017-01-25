# Test of writing servo position via Raspberry Pi GPIO pins
# Murray Ireland
# 22/12/2016

__author__ = 'Murray Ireland'

# Packages
import RPi.GPIO as GPIO
import time

# Set pin numbering scheme
GPIO.setmode(GPIO.BOARD)

# Set output pin to physical pin 11
GPIO.setup(11, GPIO.OUT)

# Set PWM sequence at 50Hz (0.02s pulse width)
pwm = GPIO.PWM(11, 50)

# Initialise PWM duty cycle
pwm.start(5)

time.sleep(1)

# Set PWM duty cycle (5% min, 10% max)
pwm.ChangeDutyCycle(10)

time.sleep(1)

# Set PWM duty cycle (5% min, 10% max)
pwm.ChangeDutyCycle(5)

time.sleep(1)

# Set PWM duty cycle (5% min, 10% max)
pwm.ChangeDutyCycle(10)

# Stop PWM
pwm.stop()

# Release pins and clean up
GPIO.cleanup()

