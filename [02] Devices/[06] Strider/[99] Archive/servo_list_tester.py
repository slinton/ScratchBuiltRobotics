#
# ServoListTester
#
# Version: 1.00
# Date: 2025-06-10
# Author: Sam Linton
#
from machine import I2C, Pin
from servo_info import ServoInfo
from servo_list import ServoList


class ServoListTester:
    
    def __init__(self, servo_list: ServoList):
        self._servo_list = servo_list
        
        
if __name__ == "__main__":
    # Create servoInfos for the front left leg
    servo_infos =[
        ServoInfo(pin=15, index=0, name='shoulder-out'),
        ServoInfo(pin=14, index=1, name='shoulder-forward'),
        ServoInfo(pin=13, index=2, name='knee'),
    ]
    for servo_info in servo_infos:
        print(servo_info)

    # Create I2C object
    i2c = I2C(id=1, scl=Pin(15), sda=Pin(14))
    print(f'Found {len(i2c.scan())} i2c devices.')

    # Create the ServoList object
    servo_list = ServoList(i2c, servo_infos)
    print(servo_list)
    
    servo_list.write(0, 90)
    servo_list.write(1, 90)
    servo_list.write(2, 90)
        