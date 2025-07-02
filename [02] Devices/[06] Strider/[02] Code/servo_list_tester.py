#
# ServoListTester
#
# Version: 1.00
# Date: 2025-06-10
# Author: Sam Linton
#
from servo_list import ServoList


class ServoListTester:
    
    def __init__(self, servo_list: ServoList):
        self._servo_list = servo_list
        
        
if __name__ == "__main__":
    # Front left leg
    servo_infos =[
        ServoInfo(index=15, name='shoulder-out'),
        ServoInfo(index=14, name='shoulder-forward'),
        ServoInfo(index=13, name='knee'),
    ]

    # Create I2C object
    i2c = I2C(id=1, scl=Pin(15), sda=Pin(14))
    print(f'Found {len(i2c.scan())} i2c devices.')

    # Create the ServoSet object
    servo_set = ServoSet(i2c, servo_infos)
    print(servo_set)
        