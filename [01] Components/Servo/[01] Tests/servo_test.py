#
# servo_test
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
#
from servo import Servo
from time import sleep

angle0: int = 10
angle1: int = 170

while True:
    answer: str = input('Input servo pin number (q to quit): ')
    if answer == 'q':
        break
    pin = int(answer)
    servo = Servo(pin)
    print(f'Servo moving to {angle0} degrees')
    servo.write(angle0)
    sleep(1)
    print(f'Servo moving to {angle1} degrees')
    servo.write(angle0)
    sleep(1)
print('Test concluded.')