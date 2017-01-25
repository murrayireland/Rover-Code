# Bluetooth controller functions
# Murray Ireland
# 06/01/2017
__author__ = 'Murray Ireland'

# Load library functions
import time, os

# Make dummy monitor
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame

# Initialise
def Init():

    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    pygame.joystick.init()

    # Number of joysticks available
    joystick_count = pygame.joystick.get_count()

    # Check number of stick axes and buttons
    if joystick_count == 0:
        print "No controllers available"
        return 0
    else:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        return joystick

# Get controls
def GetControls( joystick ):
    # Process event handlers
    pygame.event.pump()

    # Buttons
    buttons = {}
    buttons['A'] = joystick.get_button(0)
    buttons['B'] = joystick.get_button(1)
    buttons['X'] = joystick.get_button(3)
    buttons['Y'] = joystick.get_button(4)
    buttons['L1'] = joystick.get_button(6)
    buttons['R1'] = joystick.get_button(7)
    buttons['L2'] = joystick.get_button(8)
    buttons['R2'] = joystick.get_button(9)
    buttons['Select'] = joystick.get_button(10)
    buttons['Start'] = joystick.get_button(11)
    buttons['L stick'] = joystick.get_button(13)
    buttons['R stick'] = joystick.get_button(14)

    # Axes
    axes = {}
    axes['L horizontal'] = joystick.get_axis(0)
    axes['L vertical'] = joystick.get_axis(1)
    axes['R horizontal'] = joystick.get_axis(2)
    axes['R vertical'] = joystick.get_axis(3)
    #axes['R trigger'] = joystick.get_axis(4)
    #axes['L trigger'] = joystick.get_axis(5)

    # Return dictionaries
    return ( buttons, axes )
