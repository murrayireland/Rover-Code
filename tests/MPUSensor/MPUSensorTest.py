#!/usr/bin/env python

"""MPUSensorTest.py: Receives raw data from MPU 9DOF click IMU+Magnetometer and displays it."""

import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a*a) + (b*b))

def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)

def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for Revision 1 boards
address = 0x69          # Address via i2cdetect

# Now wake up the IMU as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

print "Gyro data"
print "---------"

gyro_xout = read_word_2c(0x43)
gyro_yout = read_word_2c(0x45)
gyro_zout = read_word_2c(0x47)

print "gyro_xout: {}, scaled: {}".format(gyro_xout, gyro_xout/131.0)
print "gyro_yout: {}, scaled: {}".format(gyro_yout, gyro_yout/131.0)
print "gyro_zout: {}, scaled: {}".format(gyro_zout, gyro_zout/131.0)

print
print "Accelerometer data"
print "------------------"

accel_xout = read_word_2c(0x3b)
accel_yout = read_word_2c(0x3d)
accel_zout = read_word_2c(0x3f)

accel_xout_scaled = accel_xout/16384.0
accel_yout_scaled = accel_yout/16384.0
accel_zout_scaled = accel_zout/16384.0

print "accel_xout: {}, scaled: {}".format(accel_xout, accel_xout_scaled)
print "accel_yout: {}, scaled: {}".format(accel_yout, accel_yout_scaled)
print "accel_zout: {}, scaled: {}".format(accel_zout, accel_zout_scaled)

print "x rotation: {}".format(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
print "y rotation: {}".format(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
