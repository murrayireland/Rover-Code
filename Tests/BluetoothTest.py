# Test of receiving Bluetooth controller commands on Raspberry Pi 3
# Murray Ireland
# 22/12/2016
__author__ = 'Murray Ireland'

# Load library functions
import time
import pygame
#import RPi.GPIO

# Initialise
pygame.init()
pygame.joystick.init()

# Number of joysticks available
joystick_count = pygame.joystick.get_count()

if joystick_count == 0:
    print "No controllers available"
else :
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Get the joystick name
    name = joystick.get_name()
    print "Joystick name: {}".format(name)

    # Get joystick axes
    axes = joystick.get_numaxes()
    print "Number of axes: {}".format(axes)

    # Get joystick buttons
    buttons = joystick.get_numbuttons()
    print "Number of buttons: {}".format(buttons)


if joystick_count == 1:
    while False:
        # Print axes values
        for i in range(axes):
            axis = joystick.get_axis(i)
            print "Axis {} value: {:f}".format(i, axis)

        for i in range(buttons):
            button = joystick.get_button(i)
            print "Button {} value {:f}".format(i, button)

        # Wait
        time.sleep(1)
