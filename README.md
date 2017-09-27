# Rover-Code
Code for University of Glasgow SPROG Rovers

## manual-controllers
Scripts for controlling rovers with Bluetooth wireless controller.

| Script | Description |
|-|-|
| `adafruitDriver.py` | Motor driver class file for rovers using Adafruit DC motor drivers. This includes the *Lynxmotion 4WD3* and *Bogie Runt* rovers. This script takes collective and differential speed commands and writes the motor PWM duty cycles accordingly. It also returns the applied motor voltages for saving to file. |
| `bluetoothinput.py` | Bluetooth game controller class file for all rovers. Upon import, it searches for a connected controller and initialises `pygame`. During the control loop, it receives physical commands from the gamepad and returns them as dictionaries describing the axis, button and hat positions. Default mappings are included. `print_index` can be used to define new control mappings. |
| `dagu4wd_sysid.py` | Dagu 4WD open-loop controller with series of steps in collective and differential inputs. Used for system identification. |
| `dagu4wd.py` | Dagu 4WD closed-loop controller for bluetooth game control. Includes Sense HAT and video support. |
| `dagu6wd.py` | Dagu 6WD closed-loop controller for bluetooth game control. Includes Sense HAT and video support. |
| `lynxmotion.py` | Lynxmotion 4WD3 closed-loop controller for bluetooth game control. Includes Sense HAT and video support. |
| `rockerbogie.py` | Rocker Bogie closed-loop controller for bluetooth game control. Includes Sense HAT and video support. *(Probably not working)* |
| `test_wildthumper.py` | Test script for Wild Thumper rovers and `wildthumper` class |
| `wildthumper.py` | Motor driver class file for Wild Thumper rovers. This script takes collective and differential speed commands and writes the motor PWM duty cycles accordingly. It also returns the applied motor voltages for saving to file. |

## tests

##