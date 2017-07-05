"""
bluetooth_input.py: Allows bluetooth controller to be used as input. This
script is currently tested only on a cheap Ipega gamepad.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "21/02/17"

import time
import os
import pygame

class BluetoothInput:
    
    def __init__(self, setup=False):
        """Initialise bluetooth controller object"""

        # Initilise pygame and joystick
        pygame.init()
        pygame.joystick.init()

        # Number of joysticks available
        js_count = pygame.joystick.get_count()
        
        try:
            # Return first joystick object if available, False if not
            self.js = pygame.joystick.Joystick(0)
            self.js.init()

            # Setup mode for finding control indices
            if setup == True:
                print "In setup mode"

                self.num_buttons = self.js.get_numbuttons()
                self.num_axes = self.js.get_numaxes()
                self.num_hats = self.js.get_numhats()

                print "No. buttons: {}".format(self.num_buttons)
                print "No. axes: {}".format(self.num_axes)
                print "No. hats: {}".format(self.num_hats)

            # Assign controls from joystick name
            if self.js.get_name() == "PG-9037" and setup == False:
                print "Controller detected: PG-9037"
                self.button_list, self.axis_list, self.hat_list = self.gamepad_default()
            elif setup == False:
                print "Unfamiliar controller: Using defaults"
                self.button_list, self.axis_list, self.hat_list = self.gamepad_default()

        except Exception, error:
            print "No controllers detected"
        
    def get_controls(self):
        """Update current controls"""

        # Process event handlers
        pygame.event.pump()

        # Buttons
        buttons = {}
        for button in self.button_list:
            buttons[button] = self.js.get_button(self.button_list[button])

        # Axes
        axes = {}
        for axis in self.axis_list:
            axes[axis] = self.js.get_axis(self.axis_list[axis])

        # Hats
        hats = {}
        for hat in self.hat_list:
            hats[hat] = self.js.get_hat(self.hat_list[hat])

        return buttons, axes, hats
    
    def gamepad_default(self):
        """Default gamepad settings, based on Ipega bluetooth gamepad"""

        # Button assignments to pygame indices
        button_list = {'A': 0, 'B': 1, 'X': 3, 'Y': 4, 'L1': 6, 'R1': 7,
                       'L2': 8, 'R2': 9, 'Select': 10, 'Start': 11,
                       'L stick': 13, 'R stick': 14}
        
        # Axes assignments to pygame indices
        axis_list = {'L horizontal': 0, 'L vertical': 1, 'R horizontal': 2,
                     'R vertical': 3, 'R trigger': 4, 'L trigger': 5}

        # Hat assignments to pygame indices
        hat_list = {'D pad': 0}

        return button_list, axis_list, hat_list

    def print_index(self):
        """Print index of control for later creation of control list"""

        # Process event handlers
        pygame.event.pump()

        # Buttons
        for button in range(0, self.num_buttons):
            value = self.js.get_button(button)
            if value:
                print "Button {} on".format(button)
        
        # Axes
        for axis in range(0, self.num_axes):
            value = self.js.get_axis(axis)
            if value > 0:
                print "Axis {} positive".format(axis)
            elif value < 0:
                print "Axis {} negative".format(axis)
    
        # Hats
        for hat in range(0, self.num_hats):
            value = self.js.get_hat(hat)
            if any(value) != 0:
                print "Hat {}: {}".format(hat, value)
