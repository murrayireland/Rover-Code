# Calibrate controller signals and write for use elsewhere
# Murray Ireland
# 05/01/2017
__author__ = 'Murray Ireland'

# Load library functions
import time
import pygame

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
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Get the joystick name
    name = joystick.get_name()

# Loop for showing input results
while joystick_count > 0:
    # Event processing
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

    # Print buttons if active
    if any(b > 0 for b in buttons.itervalues()):
        print buttons
    
    if any(abs(a) > 0 for a in axes.itervalues()):
        print axes

    time.sleep(0.5)
