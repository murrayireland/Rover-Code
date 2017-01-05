# Test of receiving Bluetooth controller commands on Raspberry Pi 3
# Murray Ireland
# 22/12/2016
__author__ = 'Murray Ireland'

# Load library functions
import time
import pygame
#import RPi.GPIO

# Controller labels
buttonNames = ('A', 'B', '', 'X', 'Y', '', 'L1', 'R1', 'L2', 'R2', 'Select', 'Start', '', 'L stick', 'R stick')
axisNames = ('L horizontal', 'L vertical', 'R horizontal', 'R vertical', 'L trigger', 'R trigger')

# Initialise
pygame.init()
pygame.joystick.init()

# Number of joysticks available
joystick_count = pygame.joystick.get_count()

# Check number of stick axes and buttons
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

    # Get joystick hats
    hats  = joystick.get_numhats()
    print "Number of hats: {}".format(hats)

while True and joystick_count > 0:
    # Event processing
    pygame.event.pump()

    # Show axes
    for i in range(axes):
        axis = joystick.get_axis(i)
        if axis != 0:
            # print "Axis {} value: {}".format(i, axis)
            print "Axis {} value: {}".format(axisNames[i], axis)
    
    # Show buttons
    for i in range(buttons):
        button = joystick.get_button(i)
        if button != 0:
            # print "Button {} value: {}".format(i, button)
            print "Button {} value: {}".format(buttonNames[i], button)
    
    # Show hats
    for i in range(hats):
        hat = joystick.get_hat(i)
        if hat[0] != 0 or hat[1] != 0:
            print "D-pad value: {}".format(hat)
    
    time.sleep(0.5)

