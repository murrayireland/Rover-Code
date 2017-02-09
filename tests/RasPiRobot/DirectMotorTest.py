#!/usr/bin/env python

"""DirectMotorTest.py: Test motors via RasPiRobot board v3, using direct PWM control."""

import RPi.GPIO as GPIO
import time

RIGHT_PWM_PIN = 14
LEFT_PWM_PIN = 24
LEFT_1_PIN = 17
LEFT_2_PIN = 4
RIGHT_1_PIN = 10
RIGHT_2_PIN = 25

# Initialise PWM
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_PWM_PIN, GPIO.OUT)
# GPIO.setup(RIGHT_PWM_PIN, GPIO.OUT)
GPIO.setup(LEFT_1_PIN, GPIO.OUT)
GPIO.output(LEFT_1_PIN, 0)
GPIO.setup(LEFT_2_PIN, GPIO.OUT)
GPIO.output(LEFT_2_PIN, 0)
# GPIO.setup(RIGHT_1_PIN, GPIO.OUT)
# GPIO.output(RIGHT_1_PIN, 0)
# GPIO.setup(RIGHT_2_PIN, GPIO.OUT)
# GPIO.output(RIGHT_2_PIN, 0)
pwml = GPIO.PWM(LEFT_PWM_PIN, 50)
pwml.start(5)
# pwmr = GPIO.PWM(RIGHT_PWM_PIN, 50)
# pwmr.start(5)

for i in range(5, 50, 5):
    pwml.ChangeDutyCycle(i)
    # pwmr.ChangeDutyCycle(i)
    print(i)
    time.sleep(0.5)

# Stop PWM
pwml.stop()
# pwmr.stop()

# Release pins and clean up
GPIO.cleanup()

