#!/usr/bin/env python

"""
wildthumper.py: Class definition for Wild Thumper rovers. Adafruit 16 channel PWM driver is used to control 2/3 Cytron dual channel MDD10A motor drivers.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"

import time
import Adafruit_PCA9685 as PD
import RPi.GPIO as GPIO
from numpy import sign

class WildThumper(object):

    # PWM setup
    MOTOR_FREQ = 50
    SERVO_FREQ = 50
    BIT_LENGTH = 4095

    # Rest time for motors when changing direction
    MOTOR_REST = 0.2

    # Limit acceleration / voltage command
    MAX_VRATE = 1.5

    # Gains for controller
    KCOLL = -0.8
    KDIFF = 0.4

    # Servo limits [0 1]
    ARM_MAX = 0.12
    ARM_MIN = 0.065
    GRB_OPN = 0.072
    GRB_CLS = 0.045

    # Servo speed gains
    ARM_GAIN = 0.02

    def __init__(self, num_wheels, battery_voltage, motor_voltage, debugging=0):

        # Print stuff in debugging mode
        self.debugging = debugging

        # Initialise GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Initialise time
        t0 = time.time()
        self.time_init = t0
        self.time = t0
        self.time_prev = t0
        self.motor_stop_time = t0

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
            GPIO.output(self.motor_pins[pin], self.motor_pols[pin])

        # Scale pwm commands so motor voltage isn't exceeded
        self.motor_voltage = motor_voltage
        self.battery_voltage = battery_voltage
        self.pwm_scale = float(motor_voltage)/float(battery_voltage)

    def init_4wd(self):
        """Set pin and channel allocations for 4-wheel rover"""

        # Motor direction pins
        self.motor_pins = {'BL': 17, 'BR': 18, 'FL': 6, 'FR': 12}
        
        # Motor PWM channels
        self.motor_chls = {'BL': 0, 'BR': 1, 'FL': 14, 'FR': 15}

        # Set motor polarity
        self.motor_pols = {'BL': 0, 'BR': 1, 'FL': 0, 'FR': 1}

        # Initialise motor directions as forward
        self.old_motor_dirs = {'BL': 1, 'FL': 1, 'BR': 1, 'FR': 1}

        # Set up empty dictionary for stopping motors
        self.stop_dcs = {'BL': 0, 'FL': 0, 'BR': 0, 'FR': 0}

        # Initialise motor voltages for saving
        self.motor_voltages = {'BL': 0, 'FL': 0, 'BR': 0, 'FR': 0}

        # Speeds at previous steps
        self.speeds_prev = {'L': 0, 'R': 0}
        
        # Servo PWM channels
        self.servo_chls = {'Arm': 4, 'Grabber': 5}

        # Set up PWM driver for servos
        self.servo = PD.PCA9685()
        self.servo.set_pwm_freq(self.SERVO_FREQ)

        # Initialise servo positions
        self.servo_pos = {'Arm': 0, 'Grabber': 0}

        # Scale in given range
        arm_pos = (self.ARM_MAX + self.ARM_MIN)/2
        grb_pos = self.GRB_CLS

        self.servo.set_pwm(
            self.servo_chls['Arm'],
            0, 
            int(arm_pos*self.BIT_LENGTH)
            )

        self.servo.set_pwm(
            self.servo_chls['Grabber'],
            0, 
            int(grb_pos*self.BIT_LENGTH)
            )

        time.sleep(0.5)

        # Check stuff
        # print "Motor freq: {}".format(self.motors.)

    def init_6wd(self):
        """Set pin and channel allocations for 6-wheel rover"""

        # Motor direction pins
        self.motor_pins = {'BL': 17, 'ML': 22, 'FL': 6,
                           'BR': 18, 'MR': 27, 'FR': 12}
        
        # Motor PWM channels
        self.motor_chls = {'BL': 14, 'ML': 1, 'FL': 8,
                           'BR': 15, 'MR': 0, 'FR': 9}

        # Set motor polarity
        self.motor_pols = {'BL': 1, 'ML': 1, 'FL': 1, 'BR': 0, 'MR': 0, 'FR': 0}

        # Initialise motor directions as forward
        self.old_motor_dirs = {'BL': 1, 'ML': 1, 'FL': 1, 'BR': 1, 'MR': 1, 'FR': 1}

        # Set up empty dictionary for stopping motors
        self.stop_dcs = {'BL': 0, 'ML': 0, 'FL': 0, 'BR': 0, 'MR': 0, 'FR': 0}

        # Initialise motor voltages for saving
        self.motor_voltages = {'BL': 0, 'ML': 0, 'FL': 0, 'BR': 0, 'MR': 0, 'FR': 0}

        # Speeds at previous steps
        self.speeds_prev = {'L': 0, 'R': 0}

        time.sleep(0.5)

    def update_motors(self, coll, diff):
        """Update motor speeds by calling set_motors method"""

        # Get speeds from controls
        lspeed = self.KCOLL*coll + self.KDIFF*diff
        rspeed = self.KCOLL*coll - self.KDIFF*diff

        # Get current time
        t = self.time

        # Get speeds and time at previous step
        told = self.time_prev
        lold = self.speeds_prev['L']
        rold = self.speeds_prev['R']

        # Limit speeds
        maxspeed = 1
        lspeed = lspeed*(lspeed <= maxspeed and lspeed >= -maxspeed) \
            + maxspeed*(lspeed > maxspeed) - maxspeed*(lspeed < -maxspeed)
        rspeed = rspeed*(rspeed <= maxspeed and rspeed >= -maxspeed) \
            + maxspeed*(rspeed > maxspeed) - maxspeed*(rspeed < -maxspeed)

        # Check acceleration
        if t - told == 0:
            ldot = 0
            rdot = 0
        else:
            ldot = (lspeed - lold)/(t - told)
            rdot = (rspeed - rold)/(t - told)

        # Limit voltage rate of change
        if abs(ldot) > self.MAX_VRATE:
            ldot = sign(ldot)*self.MAX_VRATE
            lspeed = lold + (t - told)*ldot
        if abs(rdot) > self.MAX_VRATE:
            rdot = sign(rdot)*self.MAX_VRATE
            rspeed = rold + (t - told)*rdot

        # Set speeds to motors
        speeds = {'BL': lspeed, 'FL': lspeed, 'BR': rspeed, 'FR': rspeed}
        if self.num_wheels == 6:
            speeds['ML'] = lspeed
            speeds['MR'] = rspeed

        # Set motor directions
        motor_dirs_out = self.set_direction( speeds )

        # Stop motors if direction changes
        motor_active = self.motor_safety_stop()

        # Set motor speeds
        self.set_speed( speeds, motor_active )

        # Save variables for next step
        self.time_prev = t
        self.speeds_prev = {'L': lspeed, 'R': rspeed}

        # Update time
        self.time = time.time()

        # Return motor voltages
        inputs = self.motor_voltages
        return inputs
        
    def set_direction( self, speeds ):
        """Set motor directions, trigger motor stop if direction has changed"""

        stop_trigger = 0

        for motor in speeds:
            dir = float(speeds[motor]) >= 0
            if dir != self.old_motor_dirs[motor]:
                stop_trigger = 1
                GPIO.output( self.motor_pins[motor], dir == self.motor_pols[motor] )
                self.old_motor_dirs[motor] = dir
        
        if stop_trigger:
            self.motor_stop_time = time.time()

    def motor_safety_stop( self ):
        """Stop motors if direction has changed"""

        # Check if time is within tolerance of initial stop time
        if time.time() - self.motor_stop_time < self.MOTOR_REST:
            motor_active = 0
        else:
            motor_active = 1

        return motor_active

    def set_speed( self, speeds, motor_active ):
        """Set motor duty cycles, based on speed command"""

        motor_dcs = {'BL': 0, 'FL': 0, 'BR': 0, 'FR': 0}

        # Get absolute speeds
        for motor in speeds:

            # Motor speed as voltage (zero if motor is not active)
            self.motor_voltages[motor] = speeds[motor] * self.motor_voltage * motor_active

            # Duty cycle from absolute voltage
            dc = int( self.BIT_LENGTH * abs(self.motor_voltages[motor]) / self.battery_voltage )
            motor_dcs[motor] = dc

            # Write duty cycle if motor is active, 0 if not
            self.motors.set_pwm( self.motor_chls[motor], 0, dc )

        # print motor_dcs

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
            motor_dirs[motor] = bool(speeds[motor] >= 0)

            # Set direction change check to prevent the motors melting
            if dir_change == False and speeds[motor] > 0.01:
                dir_change = motor_dirs[motor] != old_dirs[motor]

        if dir_change == True:
            motor_dcs = self.stop_dcs
            active_dirs = old_dirs
        else:
            active_dirs = motor_dirs
        
        # Cycle motors after checking for direction change
        for motor in self.motor_chls:
            # Set motor direction
            if self.motor_dirs[motor] < 0:
                dir = not(active_dirs[motor])
            else:
                dir = active_dirs[motor]
            
            GPIO.output(self.motor_pins[motor], dir)

            # Set motor duty cycle motors
            self.motors.set_pwm(
                    self.motor_chls[motor],
                    0,
                    motor_dcs[motor]
                )
                
        # Print motor duty cycles and directions
        if self.debugging:
            # print "Speeds: {}".format(speeds)
            print "DCs: {}, Dirs: {}".format(motor_dcs,active_dirs)
            
        # Pause if stopping motors
        if dir_change == True:
            # Pause briefly
            time.sleep(self.MOTOR_REST)
        
        # Get motor voltages
        motor_voltages = 0

        # Save motor voltages and directions
        return (motor_voltages, motor_dirs)

    def stop_motors(self):
        """Stop motors immediately"""

        print("Stopping all motors")

        for motor in self.motor_chls:
            self.motors.set_pwm(self.motor_chls[motor], 0, 0)

    def update_servos(self, arm_control, grb_control):
        """Update servo positions"""

        # Arm control sets velocity
        arm_pos = self.servo_pos['Arm']
        arm_pos = arm_pos - self.ARM_GAIN*arm_control

        # Limit to range [-1 1]
        arm_pos = arm_pos*(arm_pos >= -1 and arm_pos <= 1) - \
                  (arm_pos < -1) + (arm_pos > 1)
        self.servo_pos['Arm'] = arm_pos

        # Scale in given range
        arm_pos = (self.ARM_MAX - self.ARM_MIN)*arm_pos/2 + \
                  (self.ARM_MAX + self.ARM_MIN)/2

        # Update arm position
        self.servo.set_pwm(
            self.servo_chls['Arm'],
            0,
            int(arm_pos*self.BIT_LENGTH)
            )

        # Grabber is opened by button
        grb_pos = self.GRB_OPN*grb_control + self.GRB_CLS*(grb_control == 0)
        
        # Update grabber position
        self.servo.set_pwm(
            self.servo_chls['Grabber'],
            0,
            int(grb_pos*self.BIT_LENGTH)
            )

    def cleanup(self):
        """Cleanup GPIO pins and PWMs"""

        print("Cleaning up GPIO")

        GPIO.cleanup()
            
    def test(self):

        print "Just testing"
            