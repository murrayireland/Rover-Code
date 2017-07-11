from sense_hat import SenseHat

sense = SenseHat()

# Define colours
w = (255, 255, 255)
r = (255, 0, 0)
g = (0, 255, 0)
b = (0, 0, 255)
e = (0, 0, 0)

# Define directions
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


def arrw(c):

    return [
    e,e,e,c,c,e,e,e,
    e,e,c,c,c,c,e,e,
    e,c,c,c,c,c,c,e,
    c,c,c,c,c,c,c,c,
    e,e,e,c,c,e,e,e,
    e,e,e,c,c,e,e,e,
    e,e,e,c,c,e,e,e,
    e,e,e,c,c,e,e,e,
    ]

while True:
    for event in sense.stick.get_events():
        if event.action == "released":
            sense.set_pixels(blnk)
        else:  
            if event.direction == "up":
                sense.set_rotation(0)
                sense.set_pixels(arrw(w))
            elif event.direction == "down":
                sense.set_rotation(180)
                sense.set_pixels(arrw(r))
            elif event.direction == "right":
                sense.set_rotation(90)
                sense.set_pixels(arrw(b))
            elif event.direction == "left":
                sense.set_rotation(270)
                sense.set_pixels(arrw(g))

