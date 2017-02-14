#!/usr/bin/env python

"""
wildthumper.py: Class definition for Wild Thumper rovers. Adafruit 16 channel PWM driver is used to control 2/3 Cytron dual channel MDD10A motor drivers.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"

import time
import Adafruit_PCA9685 as PD
import RPi.GPIO as GPIO

class WildThumper(object):

    # Motor driver direction pins on RPi (BCM)
    # Drivers are numbered in increasing order back to front
    MD1_M1_PIN = 17
    MD1_M2_PIN = 18
    MD2_M1_PIN = 22
    MD2_M2_PIN = 23
    MD3_M1_PIN = 24
    MD3_M2_PIN = 25

    # Motor driver PWM channels on PWM driver
    # Drivers are numbered in increasing order back to front
    MD1_M1_CHL = 0
    MD1_M2_CHL = 1
    MD2_M1_CHL = 14
    MD2_M2_CHL = 15
    MD3_M1_CHL = 4
    MD3_M2_CHL = 5

    # Servo PWM channels on PWM driver
    S1_CHL = 8
    S2_CHL = 9

    # PWM setup
    MOTOR_FREQ = 500
    SERVO_FREQ = 20
    BIT_LENGTH = 4095

    # Rest time for motors when changing direction
    MOTOR_REST = 0.2

    # Gains for controller
    KCOLL = -0.8
    KDIFF = 0.8

    def __init__(self, num_wheels, battery_voltage, motor_voltage, debugging=0):

        # Print stuff in debugging mode
        self.debugging = debugging

        # Initialise GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Initialise GPIO for different platforms
        self.num_wheels = num_wheels
        if num_wheels == 4:
            self.init_4wd()
        elif num_wheels == 6:
            self.init_6wd()
        else:
            print("Incorrect configuration chosen, please select 4 or 6 wheels")
            return

        # Set up PWM driver for motors
        self.motors = PD.PCA9685()
        self.motors.set_pwm_freq(self.MOTOR_FREQ)

        # Initialise direction pins
        for pin in self.motor_pins:
            
            # Set pins as outputs
            GPIO.setup(self.motor_pins[pin], GPIO.OUT)

            # Set pins to high
            GPIO.output(self.motor_pins[pin], GPIO.HIGH)

        # Scale pwm commands so motor voltage isn't exceeded
        self.pwm_scale = float(motor_voltage)/float(battery_voltage)

    def init_4wd(self):
        """Set pin and channel allocations for 4-wheel rover"""

        # Motor direction pins
        self.motor_pins = {'BL': self.MD1_M1_PIN, 'FL': self.MD1_M2_PIN,
                           'BR': self.MD2_M1_PIN, 'FR': self.MD2_M2_PIN}
        
        # Motor PWM channels
        self.motor_chls = {'BL': self.MD1_M1_CHL, 'FL': self.MD1_M2_CHL,
                           'BR': self.MD2_M1_CHL, 'FR': self.MD2_M2_CHL}

        # Initialise motor directions as forward
        self.old_motor_dirs = {'BL': True, 'FL': True, 'BR': True, 'FR': True}

        # Set up empty dictionary for stopping motors
        self.stop_dcs = {'BL': 0, 'FL': 0, 'BR': 0, 'FR': 0}
        
        # Servo PWM channels
        self.servo_chls = {'Arm': self.S1_CHL, 'Grabber': self.S2_CHL}

        # Set up PWM driver for servos
        self.servo = PD.PCA9685()
        self.servo.set_pwm_freq(self.SERVO_FREQ)

    def init_6wd(self):
        """Set pin and channel allocations for 6-wheel rover"""

        # Motor direction pins
        self.motor_pins = {'BL': self.MD1_M1_PIN, 'ML': self.MD1_M2_PIN,
                           'FL': self.MD3_M1_PIN, 'BR': self.MD2_M1_PIN,
                           'MR': self.MD2_M2_PIN, 'FR': self.MD3_M2_PIN}
        
        # Motor PWM channels
        self.motor_chls = {'BL': self.MD1_M1_CHL, 'ML': self.MD1_M2_CHL,
                           'FL': self.MD3_M2_CHL, 'BR': self.MD2_M1_CHL,
                           'MR': self.MD2_M2_CHL, 'FR': self.MD3_M2_CHL}

        # Set up empty dictionary for stopping motors
        self.stop_dcs = {'BL': 0, 'ML': 0, 'FL': 0, 'BR': 0, 'MR': 0, 'FR': 0}

    def update_motors(self, coll, diff):
        """Update motor speeds by calling set_motors method"""

        # Get speeds from controls
        lspeed = self.KCOLL*coll + self.KDIFF*diff
        rspeed = self.KCOLL*coll - self.KDIFF*diff

        # Limit speeds
        maxspeed = 1
        lspeed = lspeed*(lspeed <= maxspeed and lspeed >= -maxspeed) \
            + maxspeed*(lspeed > maxspeed) - maxspeed*(lspeed < -maxspeed)
        rspeed = rspeed*(rspeed <= maxspeed and rspeed >= -maxspeed) \
            + maxspeed*(rspeed > maxspeed) - maxspeed*(rspeed < -maxspeed)

        # Set speeds to motors
        speeds = {'BL': lspeed, 'FL': lspeed, 'BR': rspeed, 'FR': rspeed}
        if self.num_wheels == 6:
            speeds['ML'] = lspeed
            speeds['MR'] = rspeed

        # Get previous motor directions
        old_dirs = self.old_motor_dirs

        # Set motors
        new_dirs = self.set_motors(speeds, old_dirs)

        # Save directions for next step
        self.old_motor_dirs = new_dirs

    def set_motors(self, speeds, old_dirs):

        """Set motor duty cycles, based on speed command in range [-1, 1]"""

        # Add error-checking for speeds input here

        # Initialise check for motor direction change
        dir_change = False

        # Initialise dictionaries
        motor_dcs = {}
        motor_dirs = {}

        # Cycle motors and get PWM and direction cmds
        for motor in self.motor_chls:

            # Duty cycle as bit length
            motor_dcs[motor] = int(self.pwm_scale*self.BIT_LENGTH
                                    *abs(speeds[motor]))

            # Direction as boolean
            motor_dirs[motor] = speeds[motor] >= 0

            # Set direction change check to prevent the motors melting
            if dir_change == False:
                dir_change = motor_dirs[motor] != old_dirs[motor]

        if dir_change == True:
            motor_dcs = self.stop_dcs
            active_dirs = old_dirs
        else:
            active_dirs = motor_dirs
        
        # Cycle motors after checking for direction change
        for motor in self.motor_chls:
                
            # Set motor direction
            GPIO.output(self.motor_pins[motor], active_dirs[motor])

            # Set motor duty cycle motors
            self.motors.set_pwm(
                    self.motor_chls[motor],
                    0,
                    motor_dcs[motor]
                )
                
        # Print motor duty cycles and directions
        if self.debugging:
            print "DCs: {}, Dirs: {}".format(motor_dcs,active_dirs)
            
        # Pause if stopping motors
        if dir_change == True:
            # Pause briefly
            time.sleep(self.MOTOR_REST)
        
        # Save motor directions
        return motor_dirs

    def stop_motors(self):
        """Stop motors immediately"""

        print("Stopping all motors")

        for motor in self.motor_chls:
            self.motors.set_pwm(self.motor_chls[motor], 0, 0)

    def cleanup(self):
        """Cleanup GPIO pins and PWMs"""

        print("Cleaning up GPIO")

        GPIO.cleanup()
            
    def test(self):

        print "Just testing"
            