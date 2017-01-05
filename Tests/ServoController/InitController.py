# Calibrate controller signals and write for use elsewhere
# Murray Ireland
# 05/01/2017
__author__ = 'Murray Ireland'

# Load library functions
import time
import pygame

# Initialise
pygame.init()
pygame.joystick.init()

# Number of joysticks available
joystick_count = pygame.joystick.get_count()

# Check number of stick axes and buttons
if joystick_count == 0:
    print "No controllers available"
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Get the joystick name
    name = joystick.get_name()