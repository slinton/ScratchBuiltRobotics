#
# RCCar
#

# Remote Control Car
from rc_car import RCCar
import uasyncio as asyncio

rc_car = RCCar(led_pin=6, buzzer_pin=22)
asyncio.run(rc_car.start())
    
    
'''
# Robot Car
robot_car = RobotCar(led_pin=6, buzzer_pin=22)
    
# Drive in a square
robot_car.buzzer.begin_sound()
robot_car.led.on()
for i in range(4):
    robot_car.forward(100, 1)
    sleep(1)
    robot_car.turn_left(100, 0.5)
    sleep(1)
robot_car.buzzer.end_sound()
robot_car.led.off()

'''
    
        
        
    
        
        
        



