import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

gpio.setwarnings(False)

# Pins
ain1 = 16
ain2 = 20
pwma = 21
bin1 = 26
bin2 = 19
pwmb = 13
stby = 12

# Battery voltage
vB = 7.4

# Motor voltage
vM = 5

## Setup

# Standby channel
gpio.setup(stby, gpio.OUT)

# PWM channels
gpio.setup(pwma, gpio.OUT)
gpio.setup(pwmb, gpio.OUT)

# Direction channels
gpio.setup(ain1, gpio.OUT)
gpio.setup(ain2, gpio.OUT)
gpio.setup(bin1, gpio.OUT)
gpio.setup(bin2, gpio.OUT)

# Set outputs
    
# Standby
gpio.output(stby, gpio.HIGH)

# PWM channels
cha = gpio.PWM(pwma,20)
chb = gpio.PWM(pwmb,20)
#gpio.output(pwma, gpio.HIGH)
#gpio.output(pwmb, gpio.HIGH)

# Write duty cycle
def writeSpeed(dc):
    cha.start(dc*vM/vB)
    chb.start(dc*vM/vB)

# Direction channels
gpio.output(ain1, gpio.HIGH)
gpio.output(ain2, gpio.LOW)
gpio.output(bin1, gpio.HIGH)
gpio.output(bin2, gpio.LOW)

t0 = time.time()
t = 0

while t < 10:
    
    # Write speed
    writeSpeed(t*10)

    t = time.time() - t0

# Stop
cha.stop()
chb.stop()



