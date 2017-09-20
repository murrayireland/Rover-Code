# Bluetooth controller functions
# Murray Ireland
# 06/01/2017
__author__ = 'Murray Ireland'

# Load module
from sense_hat import SenseHat

sense = SenseHat()

white = (255, 255, 255)
red = (255, 0, 0)

sense.show_letter("<", red)