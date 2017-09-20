#!/usr/bin/env python

"""
test_wildthumper.py: Test script for Dagu Wild Thumper 4WD.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "24/01/17"

import time
from wildthumper import WildThumper

# Initialise wild thumper control
wt4 = WildThumper(4, 7.4, 7.2, 1)

# Set controls manually
speeds = {'BL': 0, 'FL': 0.5, 'BR': 0, 'FR': 0.5}

motor_dirs_out = wt4.set_direction( speeds )
wt4.set_speed( speeds, 1 )

time.sleep(2)

speeds = {'BL': 0, 'FL': 0, 'BR': 0, 'FR': 0}

motor_dirs_out = wt4.set_direction( speeds )
wt4.set_speed( speeds, 1 )

time.sleep(1)

speeds = {'BL': 0, 'FL': -0.5, 'BR': 0, 'FR': -0.5}

motor_dirs_out = wt4.set_direction( speeds )
wt4.set_speed( speeds, 1 )

time.sleep(2)

# print("Step 1")
# axis = {'L vertical': 1, 'L horizontal': 0.2}
# wt4.update_motors(axis['L vertical'], axis['L horizontal'])

# time.sleep(1)

# print("Step 2")
# axis = {'L vertical': 1, 'L horizontal': -0.2}
# wt4.update_motors(axis['L vertical'], axis['L horizontal'])

# time.sleep(1)

# print("Step 3")
# axis = {'L vertical': 1, 'L horizontal': -0.2}
# wt4.update_motors(axis['L vertical'], axis['L horizontal'])

# time.sleep(1)

# print("Step 4")
# axis = {'L vertical': -1, 'L horizontal': -0.2}
# wt4.update_motors(axis['L vertical'], axis['L horizontal'])

# time.sleep(1)

# print("Step 5")
# axis = {'L vertical': -1, 'L horizontal': -0.2}
# wt4.update_motors(axis['L vertical'], axis['L horizontal'])

# time.sleep(1)

# Stop motors
wt4.stop_motors()

# GPIO cleanup
wt4.cleanup()
