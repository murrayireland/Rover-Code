#!/usr/bin/env python

"""
adafruitDriver.py: Class definition for Adafruit DC driver-driven rovers. Used on 4-wheel Lynxmotion 4WD3 and 6-wheel Bogie Runt rovers.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"

import time
import RPi.GPIO as GPIO

class AdafruitDriver(object):

    # Motor driver pins on RPi (BCM)
    PWMA = 21
    AIN1 = 16
    AIN2 = 20
    PWMB = 13
    BIN1 = 26
    BIN2 = 19
    STBY = 12

    # PWM setup
    PWM_FREQ = 200

    # Rest time for motors when changing direction
    MOTOR_REST = 0.2

    # Limit acceleration / voltage command
    MAX_RATE = 1.5

    # Gains for controller
    K_COLL = -0.8
    K_DIFF = 0.5

    def __init__(self, battery_voltage, motor_voltage, rover_name, debugging=0):

        # Print stuff in debugging mode
        self.DEBUGGING = debugging

        # Initialise GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Initialise time
        t0 = time.time()
        self.time = time.time()
        self.motor_stop_time = time.time()

        # Set voltages
        self.BATTERY_VOLTAGE = battery_voltage
        self.MOTOR_VOLTAGE = motor_voltage

        # Set up rover
        self.setup_rover(rover_name)
        self.motor_stop = False

        # Pin setup
        GPIO.setup(self.PWM_LEFT, GPIO.OUT)
        GPIO.setup(self.PWM_RIGHT, GPIO.OUT)
        GPIO.setup(self.DIR_LEFT_1, GPIO.OUT)
        GPIO.setup(self.DIR_LEFT_2, GPIO.OUT)
        GPIO.setup(self.DIR_RIGHT_1, GPIO.OUT)
        GPIO.setup(self.DIR_RIGHT_2, GPIO.OUT)
        GPIO.setup(self.STBY, GPIO.OUT)

        # Initialise binary outputs
        GPIO.output(self.DIR_LEFT_1, self.LEFT_POL == 1)
        GPIO.output(self.DIR_LEFT_2, self.LEFT_POL == 0)
        GPIO.output(self.DIR_RIGHT_1, self.RIGHT_POL == 1)
        GPIO.output(self.DIR_RIGHT_2, self.RIGHT_POL == 0)
        GPIO.output(self.STBY, 1)

        # Initialise PWM outputs
        self.left_pwm = GPIO.PWM(self.PWM_LEFT, self.PWM_FREQ)
        self.right_pwm = GPIO.PWM(self.PWM_RIGHT, self.PWM_FREQ)
        self.left_pwm.start(0)
        self.right_pwm.start(0)

    def setup_rover(self, rover_name):
        """Set rover-specific properties"""

        if rover_name == "Lynxmotion":
            ### Lynxmotion

            print "Setting Lynxmotion 4WD3 properties"

            # Pin allocation
            self.PWM_LEFT = self.PWMA
            self.PWM_RIGHT = self.PWMB
            self.DIR_LEFT_1 = self.AIN1
            self.DIR_LEFT_2 = self.AIN2
            self.DIR_RIGHT_1 = self.BIN1
            self.DIR_RIGHT_2 = self.BIN2

            # Motor polarities (1: CW, 0: CCW)
            self.LEFT_POL = 1
            self.RIGHT_POL = 0
            
            # Initialise motor directions at prev step (1: CW, 0: CCW)
            self.left_dir_prev = 1
            self.right_dir_prev = 1

        elif rover_name == "Bogie Runt":
            ### Bogie Runt rover

            print "Setting Bogie Runt rover properties"

            # Pin allocation
            self.PWM_LEFT = self.PWMA
            self.PWM_RIGHT = self.PWMB
            self.DIR_LEFT_1 = self.AIN1
            self.DIR_LEFT_2 = self.AIN2
            self.DIR_RIGHT_1 = self.BIN1
            self.DIR_RIGHT_2 = self.BIN2

            # Motor polarities (1: CW, 0: CCW)
            self.LEFT_POL = 1
            self.RIGHT_POL = 1
            
            # Initialise motor directions at prev step (1: CW, 0: CCW)
            self.left_dir_prev = 1
            self.right_dir_prev = 1

    def update_motors(self, coll, diff):
        """Update motor speeds"""

        # Get speeds from controls
        left_speed = self.K_COLL*coll + self.K_DIFF*diff
        right_speed = self.K_COLL*coll - self.K_DIFF*diff

        # Get directions from controls
        left_dir = left_speed >= 0
        right_dir = right_speed >= 0

        # Get current time
        t = self.time

        # Set directions
        left_dir_out, right_dir_out = self.set_direction(left_dir, right_dir)

        # Stop motors if direction has changed
        motor_stop = self.motor_safety_stop()

        # Set speeds
        left_voltage_out, right_voltage_out = self.set_speed(left_speed, right_speed)

        # Return motor voltages
        voltage_left = left_dir_out * left_voltage_out
        voltage_right = right_dir_out * right_voltage_out
        if motor_stop:
            voltage_inputs = (0, 0)
        else:
            voltage_inputs = (voltage_left, voltage_right)

        return voltage_inputs

    def set_direction(self, left_dir, right_dir):
        """Set motor directions, 1 for forward, 0 for reverse"""

        # Update motor stop time if direction has changed
        if left_dir != self.left_dir_prev or \
           right_dir != self.right_dir_prev:
            self.motor_stop_time = time.time()

        # Set left motor
        GPIO.output(self.DIR_LEFT_1, left_dir == self.LEFT_POL)
        GPIO.output(self.DIR_LEFT_2, left_dir != self.LEFT_POL)

        # Set right motor
        GPIO.output(self.DIR_RIGHT_1, right_dir == self.RIGHT_POL)
        GPIO.output(self.DIR_RIGHT_2, right_dir != self.RIGHT_POL)

        # Save directions for next iteration
        self.left_dir_prev = left_dir
        self.right_dir_prev = right_dir

        # Return directions for output
        if left_dir:
            left_dir_out = 1
        else:
            left_dir_out = -1
        
        if right_dir:
            right_dir_out = 1
        else:
            right_dir_out = -1

        return ( left_dir_out, right_dir_out )

    def set_speed(self, left_speed, right_speed):
        """Set motor speed by PWM"""

        # Get absolute speeds
        left_speed = abs(left_speed)
        right_speed = abs(right_speed)

        # Limit max speed
        left_speed = left_speed * (left_speed <= 1) + \
                     1 * (left_speed > 1)
        right_speed = right_speed * (right_speed <= 1) + \
                      1 * (right_speed > 1)

        # Update motor speeds
        self.left_pwm.ChangeDutyCycle(100 * left_speed * self.MOTOR_VOLTAGE / self.BATTERY_VOLTAGE)
        self.right_pwm.ChangeDutyCycle(100 * right_speed * self.MOTOR_VOLTAGE / self.BATTERY_VOLTAGE)

        # Return voltages for output
        return ( left_speed * self.MOTOR_VOLTAGE, right_speed * self.MOTOR_VOLTAGE )

    def motor_safety_stop(self):
        """Stop motors briefly if direction is changed"""

        # Check if time is within tolerance of initial stop time
        if time.time() - self.motor_stop_time < self.MOTOR_REST:
            motor_stop = True
            GPIO.output(self.STBY, 0)
            #print "Stopping motor"
        else:
            motor_stop = False
            GPIO.output(self.STBY, 1)

        return motor_stop

    def cleanup(self):
        """Cleanup when controller is deactivated"""

        print "Stopping all motors and cleaning up GPIO"

        self.left_pwm.stop()
        self.right_pwm.stop()
        GPIO.cleanup()
