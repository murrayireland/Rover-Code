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
dirs = {'BL': False, 'FL': False, 'BR': False, 'FR': False}

speeds = {'BL': -0.8, 'FL': -0.8, 'BR': -0.5, 'FR': -0.5}
dirs = wt4.set_motors(speeds,dirs)

time.sleep(2)

speeds = {'BL': 0.8, 'FL': 0.8, 'BR': -0.5, 'FR': -0.5}
dirs = wt4.set_motors(speeds,dirs)
dirs = wt4.set_motors(speeds,dirs)

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
