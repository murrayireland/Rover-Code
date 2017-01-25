#!/usr/bin/env python

"""MPURollPitch.py: Receives raw data from MPU 9DOF click IMU+Magnetometer and calculates roll and pitch angles."""

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

def get_angle_roll(x, y, z):
    radians = math.atan2(y, z)
    return math.degrees(radians)

def get_angle_pitch(x, y, z):
    radians = -math.atan2(x, dist(y, z))
    return math.degrees(radians)

bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for Revision 1 boards
address = 0x69          # Address via i2cdetect

# Now wake up the IMU as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

try:
    while True:

        # Get accelerometer data
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)

        # Scale data to m/s2
        accel_xout_scaled = accel_xout/16384.0
        accel_yout_scaled = accel_yout/16384.0
        accel_zout_scaled = accel_zout/16384.0

        # Get roll and pitch angles
        roll = get_angle_roll(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        pitch = get_angle_pitch(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

        # Print
        # print "Roll: {:.2f} deg, Pitch: {:.2f} deg".format(roll, pitch)
        print "Acceleration - x: {:.2f}, y: {:.2f}, z: {:.2f}".format(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

except KeyboardInterrupt:
    pass
