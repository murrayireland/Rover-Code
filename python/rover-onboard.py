#!/usr/bin/env python
""" Rover - Control of SPROG Rovers """
""" rover.py: Script that reads a IMU (naze32), reads information from a simulink ground station, 
              sends IMU data via UDP to the same ground station and logs all information. """

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2017 Altax.net"

__license__ = "GPL"
__version__ = "0.5"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

import time, datetime, csv, threading, socket, struct
import modules.UDPserver as udp
from modules.pyMultiwii import MultiWii

# Main configuration
logging = True
update_rate = 0.01 # 100 hz loop cycle

# Ground station
gs_ip = "localhost" # Change IP to the Simulink Ground Station
gs_port = 51002
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# IMU initialization
imu = MultiWii("/dev/tty.SLAB_USBtoUART") # Change port according to the USB port connected to the rover

# Main threaded function, this one reads the IMU and sends information to the ground station
def control():
    global imu

    while True:
        if udp.active:
            print "UDP server is active..."
            break
        else:
            print "Waiting for UDP server to be active..."
        time.sleep(0.5)

    try:
        if logging:
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%m_%d_%H-%M-%S')+".csv"
            f = open("logs/rov-"+st, "w")
            logger = csv.writer(f)
            logger.writerow(('timestamp','ax','ay','ay','gx','gy','gz','mx','my','mz', \
                             'udp_1','udp_2','udp_3','udp_4','udp_5','udp_6','udp_7' ))
        while True:
            # Variable to time the loop
            current = time.time()
            elapsed = 0

            # Get IMU data 
            imu.getData(MultiWii.RAW_IMU)


            # Do stuff here


            # Send information to the ground station
            message = (float(imu.rawIMU['timestamp']), \
                       float(imu.rawIMU['ax']), float(imu.rawIMU['ay']), float(imu.rawIMU['az']), \
                       float(imu.rawIMU['gx']), float(imu.rawIMU['gy']), float(imu.rawIMU['gz']), \
                       float(imu.rawIMU['mx']), float(imu.rawIMU['my']), float(imu.rawIMU['mz']))
            s = struct.Struct('>'+'d'*len(message))
            packet = s.pack(*message)
            sock.sendto(packet, (gs_ip, gs_port))

            # Logging
            row =   (time.time(), \
                    #imu.attitude['angx'], imu.attitude['angy'], imu.attitude['heading'], \
                    imu.rawIMU['ax'], imu.rawIMU['ay'], imu.rawIMU['az'], \
                    imu.rawIMU['gx'], imu.rawIMU['gy'], imu.rawIMU['gz'], \
                    imu.rawIMU['mx'], imu.rawIMU['my'], imu.rawIMU['mz'], \
                    udp.message[0], udp.message[1], udp.message[2], udp.message[3], \
                    udp.message[4], udp.message[5], udp.message[6] )
            if logging:
                logger.writerow(row)

            # Print stuff just to debug...
            #print udp.message
            print imu.rawIMU

            # Wait until the update_rate is completed 
            while elapsed < update_rate:
                elapsed = time.time() - current

    except Exception,error:
        print "Error in control thread: "+str(error)

if __name__ == "__main__":
    try:
        controlThread = threading.Thread(target=control)
        controlThread.daemon=True
        controlThread.start()
        udp.startTwisted()
    except Exception,error:
        print "Error on main: "+str(error)
        imu.ser.close()
    except KeyboardInterrupt:
        print "Keyboard Interrupt, exiting."
        exit()