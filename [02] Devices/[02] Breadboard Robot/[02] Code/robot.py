#
# Robot
#
# Version: 1.0
# Date: 2025-08-10
# Author Sam Linton
# Description: This is the class that allows programming a breadboard
# Robot
#
from time import sleep
from machine import Pin, I2C
from imu import MPU6050
from drive_train_2 import DriveTrain
from distance_sensor import DistanceSensor
from buzzer import Buzzer


class Robot:
    def __init__(self,
                 left_pins=(10, 11),
                 right_pins=(12, 13),
                 i2c_num = 0, sda_pin = 0, scl_pin = 1,
                 trig=20, echo=21,
                 buzzer_pin = 10) -> None:
        
        # Create the drive train
        i2c = I2C(i2c_num, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400_000)
        imu = MPU6050(i2c)
        self._drive_train = DriveTrain(left_pins=left_pins, right_pins=right_pins, imu=imu, frequency=20_000)
        
        # Create the distance sensor
        self._distance_sensor = DistanceSensor(trig, echo)
        
        # Buzzer
        self._buzzer = Buzzer(buzzer_pin)
        
    @property
    def drive_train(self) -> DriveTrain:
        return self._drive_train
    
    @drive_train.setter
    def drive_train(self, value):
        self._drive_train = value
    
    @property
    def distance_sensor(self) -> DistanceSensor:
        return self._distance_sensor
    
    @property
    def buzzer(self) -> Buzzer:
        return self._buzzer
    
    
if __name__ == '__main__':
    robot = Robot()
    robot.buzzer.begin_sound()
    robot.drive_train.forward(time = 1.0)
    for _ in range(100):
        print(robot.distance_sensor.get_distance_cm())
        sleep(0.1)
    robot.buzzer.end_sound()
    
    
    