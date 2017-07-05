"""
CameraTest.py: Test script for recording and saving camera imagery to memory card.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "21/02/2017"

import picamera
import datetime
d = datetime.datetime.now()
filename = "{}-{}-{}_{}-{}.h264".format(d.year, d.month, d.day, d.hour, d.minute)

camera = picamera.PiCamera()
camera.resolution = (1920, 1080)
camera.start_recording(filename)
camera.wait_recording(10)
camera.stop_recording()