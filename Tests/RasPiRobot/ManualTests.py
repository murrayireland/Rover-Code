
import time
from rrb3 import *

rr = RRB3(7.4, 6)

# LED test
rr.set_led1(0)
rr.set_led2(0)

# Initialise time
TimeInit = time.time()
Time = TimeInit

# Motor test
while Time - TimeInit < 5:

    # Update time
    Time = time.time()

    # Set motors (Rsp,Rdir,Lsp,Ldir)
    rr.set_motors(0,0,1,1)
