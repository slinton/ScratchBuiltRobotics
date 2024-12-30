#
# RobotCar
#
# Version 24_12_26_01
#
from machine import Pin
import uasyncio as asyncio
from drive_train import DriveTrain
from buzzer import Buzzer
from time import sleep

class RobotCar:
    """Contains logic for an autonomously driven car.
    """
    def __init__(self, left_pins=(10, 11), right_pins=(12, 13), led_pin: int=None, buzzer_pin:int=None)-> None:
        self.running = False
        self.led = None if led_pin == None else Pin(led_pin, Pin.OUT)
        self.buzzer = None if buzzer_pin == None else Buzzer(pin=buzzer_pin)
        self.drive_train = DriveTrain(left_pins, right_pins)
        
    def move(self, left_speed: int, right_speed: int, time_sec: float)-> None:
        """Arbitrary motion, controlling the speed of each motor independently.

        Args:
            left_speed (int): speed of the robot in the range -100 to 100
            right_speed (int): speed of the robot in the range -100 to 100
            time_sec (float): number of seconds
        """
        self.drive_train.move(left_speed, right_speed)
        sleep(time_sec)
        self.drive_train.stop()
        
    def forward(self, speed: int, time_sec: float)-> None:
        """Drive the robot forward at a given speed.

        Args:
            speed (int): speed of the robot in the range (-100, +100)
            time_sec (float): number of seconds
        """
        
        self.drive_train.forward(speed)
        sleep(time_sec)
        self.drive_train.stop()
        
    def backward(self, speed: int, time_sec: float)-> None:
        """Drive the robot backward at a given speed.

        Args:
            speed (int): backwards speed of the robot in the range (-100, +100)
            time_sec (float): number of seconds
        """
        
        self.drive_train.backward(speed)
        sleep(time_sec)
        self.drive_train.stop()
    
    def turn_left(self, speed: int, time_sec: float)-> None:
        """Turn the robot left at a given speed.

        Args:
            speed (int): speed of the robot in the range 0-100
            time_sec (float): number of seconds
        """
        
        self.drive_train.turn_left(speed)
        sleep(time_sec)
        self.drive_train.stop()
        
    def turn_right(self, speed: int, time_sec: float)-> None:
        """Turn the robot right at a given speed.

        Args:
            speed (int): speed of the robot in the range 0-100
            time_sec (float): number of seconds
        """
        
        self.drive_train.turn_right(speed)
        sleep(time_sec)
        self.drive_train.stop()
        

if __name__ == '__main__':
    robot_car = RobotCar(led_pin=9, buzzer_pin=22)
    
    # Drive in a square
    for i in range(4):
        robot_car.forward(100, 1)
        sleep(1)
        robot_car.turn_left(100, 0.5)
        sleep(1)
    
   
   
    
        
        
    
        
        
        




