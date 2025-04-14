#
# main for BLEJoystickController
#
# Version 24_07_31_01
#
from machine import Pin, I2C
from time import sleep
from ble_joystick_controller import BLEJoystickController

if __name__ == '__main__':
    try:
        i2c = I2C(0, scl=1, sda=0, freq=200_000)
        joystickController = BLEJoystickController(name="JoystickController", i2c=i2c, left=2, right=3, led=6, debug=True)
        joystickController.start()
    
    except KeyboardInterrupt:
        print('Program terminated')
