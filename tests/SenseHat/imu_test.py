from sense_hat import SenseHat
from numpy import sign

sense = SenseHat()

e = (0, 0, 0)

blnk = [
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
]

sense.set_rotation(270)

def correct(r,p,y):
    if r > 180:
        r = r - 360
    r = -r
    if p > 180:
        p = p - 360
    p = -p
    if y > 180:
        y = y - 360
         
    return r,p,y

def level(r,p,y):
    if abs(r) > 90:
        r = 90*sign(r)
    if abs(p) > 90:
        p = 90*sign(p)
    a = r*4//90 + 4
    b = p*4//90 + 4
    c = 0
    print "({0}, {1}, {2})".format(r,p,y)
##    print "({0}, {1}, {2})".format(a,b,c)
    sense.set_pixels(blnk)
    sense.set_pixel(a,b,255,0,0)

while True:
    o = sense.get_orientation()
    r = o['roll']
    p = o['pitch']
    y = o['yaw']
    r,p,y = correct(r,p,y)
    level(r,p,y)
    
