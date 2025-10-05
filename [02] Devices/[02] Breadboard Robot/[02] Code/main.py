from machine import I2C, Pin
from imu import MPU6050
from robot import Robot
from drive_train_2 import DriveTrain
from buzzer import Buzzer
from distance_sensor import DistanceSensor
from time import sleep

def square() -> None:
    robot = Robot()
    robot.buzzer.begin_sound()
    sleep(1)

    for _ in range(4):
        robot.drive_train.move_by(10)
        sleep(1)
        robot.drive_train.turn_by(90)
        sleep(1)
    
    robot.buzzer.end_sound()
    
def rhumba() -> None:
    robot = Robot()
    robot.buzzer.begin_sound()
    sleep(1)
    
    robot.drive_train.forward()
    
    while robot.distance_sensor.get_distance_cm() > 20:
        sleep(0.1)
        
    robot.drive_train.stop()
    sleep(1)
    
    robot.drive_train.move_by(-10)
    robot.drive_train.turn_by(45)
    
def test_turns() -> None:
    robot = Robot()
    dt = robot.drive_train
    dt.stop()

    robot.buzzer.begin_sound()
    sleep(2)
    
    angle = 45
    print(f'Turn by {angle}')
    dt.turn_by(angle)
    sleep(2)
    
    angle = -45
    print(f'Turn by {angle}')
    dt.turn_by(angle)
    sleep(2)
        
    dt.stop()

    
def run_tests_4():
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)
    imu = MPU6050(i2c)
    dt = DriveTrain(imu = imu)
    print(repr(dt))
    sleep(2)
    
    angle = 45
    print(f'Turn by {angle}')
    dt.turn_by(angle)
    sleep(2)
    
    angle = -45
    print(f'Turn by {angle}')
    dt.turn_by(angle)
    sleep(2)
        
    dt.stop()

if __name__ == '__main__':
    run_tests_4()