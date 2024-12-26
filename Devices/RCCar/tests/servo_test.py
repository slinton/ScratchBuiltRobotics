from servo import Servo
from time import sleep


servo1 = Servo(pin_id=16)
servo2 = Servo(pin_id=17)

while True:
    print('.')
    servo1.write(10)
    sleep(0.5)
    servo1.write(170)
    sleep(0.5)
    servo2.write(10)
    sleep(0.5)
    servo2.write(170)
    sleep(0.5)
    
