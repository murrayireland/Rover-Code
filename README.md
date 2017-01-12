# Rover-Code
Code for University of Glasgow SPROG Rovers



## python 

Inside this folder, there is a common structure that will make an asynchronous communication between two computer systems.

* The first system will be a linux computer that will be on-board the rover. Such computer will have connected a naze32 via USB. It has to then execute the script called ```rover-onboard-py```. This script is a threaded structure that has at the moment three responsibilities. The first one is to read all of the information that is sent to it via UDP (data from the ground station). The second one is to ask the naze32 for the raw IMU data. The third is to send data to the ground station. The main loop runs at 100Hz. Both computers must be in the same wireless network.

* The second computer system is a ground station running a Simulink model that reads and sends data. It will be later replaced with the main control structure.

## To-do:

- Test the python structure on the rover and ensure the data rate is fast
- Send proper data to the rover rather than sin values