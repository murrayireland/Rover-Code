"""
StreamTest.py: Test script for streaming camera imagery across network.
"""

__author__  = "Murray Ireland"
__email__   = "murray@murrayire.land"
__date__    = "21/02/2017"

import socket
import picamera
import time

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10

# Server setup
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8000))
server_socket.listen(0)

# Accept a single connection and make a file out of it
connection = server_socket.accept()[0].makefile('wb')

print "Recording"

# try:
# Start recording and send for 30 seconds
camera.start_recording(connection, format="h264")
camera.wait_recording(30)
camera.stop_recording()
# finally:
connection.close()
server_socket.close()

print "Stopping"