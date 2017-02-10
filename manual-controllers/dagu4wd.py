#!/usr/bin/env python

"""
dagu4wd.py: Manual controller for Dagu Wild Thumper 4WD. Bluetooth
controller is used to provide remote control of rover.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "24/01/17"

import wildthumper as wt

WT = wt.WildThumper(4, 7.4, 6, 1)

for speed in range(-10, 10, 1):

    print "Speed: {}".format(speed*0.1)

    LSpeed = 1
    RSpeed = speed*-0.1

    speeds = {'BL': LSpeed, 'FL': LSpeed, 'BR': RSpeed, 'FR': RSpeed}

    WT.set_motors(speeds)
