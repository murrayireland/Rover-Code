
import time
from rrb3 import *

rr = RRB3(7.4, 7.2)

# LED test
rr.set_led1(1)
rr.set_led2(1)

# Initialise time
TimeInit = time.time()
Time = TimeInit

# Motor test
while Time - TimeInit < 5:

    # Update time
    Time = time.time()

    # Set motors (Lsp,Ldir,Rsp,Rdir)
    rr.set_motors(1,0,1,0)

# LEDs off
rr.set_led1(0)
rr.set_led2(0)