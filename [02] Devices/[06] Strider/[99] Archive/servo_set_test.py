#
# servo_set_test
#
# Version: 1.00
# Date: 2025-06-10
# Author: Sam Linton
#
from servo_set import ServoSet
from servo_info import ServoInfo
from machine import I2C, Pin
from gesture import Gesture
from time import sleep
import asyncio

def home(servo_set: ServoSet) -> None:
    """Move servos to home position."""
    print('Moving to home position...', end='')
    servo_set.move_to_angles([(0, 30), (1, 30), (2, -45)], time=1.0)
    print('done.')
    sleep(1)

def print_servo_infos(servo_infos: list[ServoInfo]) -> None:
    """Print the servo information."""
    print('Servo Information:')
    for servo_info in servo_infos:
        print(servo_info)

def move_to_angles_test(servo_set: ServoSet) -> None:
    """Test moving servos to specific angles."""
    print('Moving to specific angles...', end='')
    time = 0.1
    servo_set.move_to_angles([(0, 30), (1, 30), (2, -45)], time=time)
    servo_set.move_to_angles([(0, 40), (1, 40), (2, -45)], time=time)
    servo_set.move_to_angles([(0, 40), (1, 40), (2,  00)], time=time)
    servo_set.move_to_angles([(0, 40), (1, 40), (2,  45)], time=time)
    servo_set.move_to_angles([(0, 20), (1, 20), (2,  45)], time=time)
    servo_set.move_to_angles([(0, 20), (1, 20), (2,  00)], time=time)
    servo_set.move_to_angles([(0, 20), (1, 20), (2, -45)], time=time)
    servo_set.move_to_angles([(0, 30), (1, 30), (2, -45)], time=time)
    print('done.')

def test_execute_gesture() -> None:
    print('Testing execute_gesture')
    sleep(1)

    walk_gesture: Gesture = Gesture(
        [
            [ 30,  40, 40, 40, 20,  20,  20,  30],
            [ 30,  40, 40, 40, 20,  20,  20,  30],
            [-45, -45, 00, 45, 45,  00, -45, -45]
        ]
    )

    print('Starting walk gesture...', end='')
    asyncio.run(servo_set.async_execute_gesture(walk_gesture, time=2.0, numsteps=200, repeat=5))
    print('done.')


if __name__ == "__main__":

    # Create ServoInfo array for a legged robot with 3 servos: lower-leg, upper-leg, and shoulder.
    servo_infos =[
        ServoInfo(index=0, servo_angle_0 = 107, sign = -1, name='lower-leg', angle_start=0, angle_end=90),
        ServoInfo(index=1, servo_angle_0 = 20, sign = 1, name='upper-leg', angle_start=0, angle_end=90),
        ServoInfo(index=2, servo_angle_0 = 125, sign = -1, name='shoulder', angle_start=-50, angle_end=50),
    ]

    # Create I2C object
    i2c = I2C(id=1, scl=Pin(15), sda=Pin(14))
    print(f'Found {len(i2c.scan())} i2c devices.')

    # Create the ServoSet object
    servo_set = ServoSet(i2c, servo_infos)
    print(servo_set)
        
    # Print servo information
    home(servo_set)
    
    # Test the move_to_angles method
    move_to_angles_test(servo_set)
    sleep(1)

    # Test the execute_gesture method
    test_execute_gesture()
    sleep(1)