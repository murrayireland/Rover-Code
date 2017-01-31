"""
Dagu4WDTest.py: Test of motors and servos on Dagu Wild Thumper 4WD. PWM commands are written via the 
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "24/01/17"

# Import libraries
import time
import RPi.GPIO as GPIO         # To control motor direction
import Adafruit_PCA9685 as PD   # To control outputs on PWM driver

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Disable warnings
GPIO.setwarnings(False)

# Set direction channels
Motors_Dir = {'Front-left': 17, 'Front-right': 18}

# Set PWM channels
Motors_PWM = {'Front-left': 0, 'Front-right': 1}

# Set up direction pins
for pin in Motors_Dir:
    GPIO.setup(Motors_Dir[pin], GPIO.OUT)
    GPIO.output(Motors_Dir[pin], GPIO.LOW)

# Set up PWM channels
PWM_Freq = 50  # PWM frequency (Hz)
DC_min = 0      # Min duty cycle (%)
DC_max = 100    # Max duty cycle (%)
PWM = PD.PCA9685()
PWM.set_pwm_freq(PWM_Freq)

# Set PWM from duty cycle
def set_pwm_dc(channel, on_dc, off_dc):
    # Scale on/off parameters
    on_bits = int(round((on_dc/100.0)*4095))
    off_bits = int(round((off_dc/100.0)*4095))

    # Set PWM for channel
    PWM.set_pwm(channel, on_bits, off_bits)

# Test each motor in turn
for motor in Motors_PWM:
    set_pwm_dc(Motors_PWM[motor], 0, DC_max)
    time.sleep(1)
    set_pwm_dc(Motors_PWM[motor], 0, DC_min)
    time.sleep(1)
    GPIO.output(Motors_Dir[motor], GPIO.HIGH)
    set_pwm_dc(Motors_PWM[motor], 0, DC_max)
    time.sleep(1)
    set_pwm_dc(Motors_PWM[motor], 0, DC_min)

# Clean up GPIO
GPIO.cleanup()