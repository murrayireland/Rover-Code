"""
VoltageLimit.py: Test for limiting rate and magnitude of voltage
signal to rover.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "20/02/2017"

import time
from numpy import sign

Vmax = 1
Vdotmax = 2
Vold = 0

t0 = time.time()
t = 0

while t < 6:
    # Set voltage
    if t < 1:
        V = 0
    elif t < 4:
        V = 1
    elif t < 7:
        V = -1
    elif t < 10:
        V = 0.5
    else:
        V = -0.5
    
    # Limit voltage
    if t == 0:
        Vdot = 0
    else:
        Vdot = (V - Vold)/(t - told)
    
    # Get voltage
    if abs(Vdot) > Vdotmax:
        Vdot = sign(Vdot)*Vdotmax
        V = Vold + (t - told)*Vdot

    # Reassign variables
    Vold = V
    told = t

    # Print results
    print "Time: {:5.2f}s, V: {:5.2f}V, Vdot: {:5.2f}V/s".format(t, V, Vdot)

    # Sleep
    time.sleep(0.1)

    # Get new time
    t = time.time() - t0