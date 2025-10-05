#
# DriveTrain
#
# Version: 2.00
# Date: 2025-08-02
# Author: Sam Linton
# Description:  This module controls a drive train with 2 motors using a motor driver DRV8833.
#
#
from machine import Pin, PWM, I2C
from time import sleep, ticks_us
from imu import MPU6050


class DriveTrain:
    """Class to control a drive train with 2 motors using a motor driver.
    The motor driver is controlled using PWM signals to control the speed and
    direction of the motors. 
    """
    
    MAX_DUTY_CYCLE: int = 65535
    
    def __init__(self,
                 left_pins=(10, 11),
                 right_pins=(12, 13),
                 imu: MPU6050 = None,
                 frequency: int=20_000)-> None: 
        """Initialize the DriveTrain object with the pins for the motors. Optionally 
        set the frequency of the PWM signal.

        Args:
            left_pins (Tuple[int]): PWM pin numbers for left motor
            right_pins (Tuple[int]): PWM pin numbersfor right motor
            frequency (int, optional): frequency of PWM signal (Hz). Defaults to 20_000.
        """
        
        # Create the PWM objects for the motor driver
        self.left_1 = PWM(Pin(left_pins[0], Pin.OUT), frequency)
        self.left_2 = PWM(Pin(left_pins[1], Pin.OUT), frequency)
        self.right_1 = PWM(Pin(right_pins[0], Pin.OUT), frequency)
        self.right_2 = PWM(Pin(right_pins[1], Pin.OUT), frequency)
        
        self._speed = 20.0
        
        self._turn_rate = 500.0
        self._imu = imu
        if self._imu is None:
            print('>>>>>>>>>>>>> imu is None')
            
    def move(self, left_speed: int, right_speed: int, time: float = None)-> None:
        """Arbitrary motion, controlling the speed of each motor independently.

        Args:
            left_speed (int): speed of the robot in the range -100 to 100
            right_speed (int): speed of the robot in the range -100 to 100
        """
        if left_speed > 0:
            self.left_1.duty_u16(self._speed_to_duty_cycle(left_speed))
            self.left_2.duty_u16(0)
        else:
            self.left_1.duty_u16(0)
            self.left_2.duty_u16(self._speed_to_duty_cycle(-left_speed))
            
        if right_speed > 0:
            self.right_1.duty_u16(self._speed_to_duty_cycle(right_speed))
            self.right_2.duty_u16(0)
        else:
            self.right_1.duty_u16(0)
            self.right_2.duty_u16(self._speed_to_duty_cycle(-right_speed))
            
            
        if time is not None:
            sleep(time)
            self.stop()
        
    def forward(self, speed: int=100, time: float = None)-> None:
        """Drive the robot forward at a given speed.

        Args:
            speed (int): speed of the robot in the range (-100, +100)
        """
        print('forward')
       
        
        self.move(speed, speed, time)
        
    def backward(self, speed: int=100, time: float = None)-> None:
        """Drive the robot backward at a given speed.

        Args:
            speed (int): backwards speed of the robot in the range (-100, +100)
        """
        self.move(-speed, -speed, time)
        
    def move_by(self, distance: float) -> None:
        speed = 100
        time = distance / self._speed
        self.move(speed, speed, time)
        
    def turn_left(self, speed: int = 100, time: float = None)-> None:
        """Turn the robot left at a given speed.

        Args:
            speed (int): speed of the robot in the range 0-100
        """
        
        self.move(-speed, speed, time)
        
    def turn_right(self, speed: int = 100, time: float = None)-> None:
        """Turn the robot right at a given speed.

        Args:
            speed (int): speed of the robot in the range 0-100
        """
        
        self.move(speed, -speed, time)
        
    def turn_by(self, angle: float, speed: int = 70) -> None:
        print(f'Turn {angle} degrees with speed {speed}')
        
        if self._imu is None:
            time = angle / self._turn_rate
            self.turn_right(speed = speed, time = time)
            return
        
        ang = 0.0
        sign = 1 if angle > 0.0 else -1
        #rot_ref = self._imu.gyro.z
        rot_ref = 0
        print(f'rot_ref: {rot_ref}')
        t = ticks_us()
        
        self.move(sign * speed, -sign * speed)
        
        while sign*ang < sign*angle:
            rot_raw = self._imu.gyro.z
            rot = rot_raw - rot_ref
            if abs(rot) < 1.0: rot = 0.0
            
            tn = ticks_us()
            dt = 1.0e-06 * (tn - t)
            ang -=  dt * rot
            
            t = tn
            print(f'{rot_raw} {rot} {ang}')
            sleep(0.01)
            
        self.stop()
        
    def _speed_to_duty_cycle(self, speed: int)-> int:
        """Convert a speed (0-100) to a duty cycle. The speed is clamped
        to the range 0-100

        Args:
            speed (int): speed of the robot in the range 0-100

        Returns:
            int: duty cycle in the range 0-65535
        """
        
        # TODO: may need to have minimum duty cycle to get the motors to start
        speed = max(0, min(100, speed))
        return int(DriveTrain.MAX_DUTY_CYCLE * speed / 100)
    
    def stop(self)-> None:
        """Stop the robot by setting the speed of both motors to 0.
        """
        print('stop')
        self.move(0, 0)
        
    def print_state(self)-> None:
        """Print the state of the motors.
        """
        print("Left 1: ", self.left_1.duty_u16())
        print("Left 2: ", self.left_2.duty_u16())
        print("Right 1: ", self.right_1.duty_u16())
        print("Right 2: ", self.right_2.duty_u16())
        
    def __repr__(self) -> str:
        return f"DriveTrain:\n left: {self.left_1} {self.left_2} \n right: {self.right_1} {self.right_2}"
   
  
def run_tests_4():
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)
    imu = MPU6050(i2c)
    dt = DriveTrain(imu = imu)
    print(repr(dt))
    sleep(2)
    
#     distance = 1.0
#     print(f'Move by {distance}')
#     dt.move_by(distance)
#     sleep(2)
    
    angle = 45
    print(f'Turn by {angle}')
    dt.turn_by(angle)
    sleep(2)
    
    angle = -45
    print(f'Turn by {angle}')
    dt.turn_by(angle)
    sleep(2)
        
    dt.stop()
    
def run_tests_3():
    dt = DriveTrain()
    print(repr(dt))
    sleep(1)
    
    for speed in range(50, 100, 5):
        print(speed)
        dt.forward(speed)
        sleep(1)
        
    dt.stop()
        
def run_tests_2():
    dt = DriveTrain()
    print(repr(dt))
    sleep(1)
    
    # Test the forward method
    print("Testing forward method with time")
    dt.forward(100, time = 2.0)
    sleep(2)
    
    # Test the backward method
    print("Testing backward method")
    dt.backward(100, time = 2.0)
    sleep(2)
    
    # Test the turn_left method
    print("Testing turn_left method")
    dt.turn_left(100, time = 2.0)
    sleep(2)
    
    # Test the turn_right method
    print("Testing turn_right method")
    dt.turn_right(100, time = 2.0)
    sleep(2)
    
    print('Testing complete')
    
        
def run_tests_1():
    print('Testing DriveTrain class')
    # Create the DriveTrain object
    #dt = DriveTrain((1, 2), (3, 4))
    dt = DriveTrain()
    print(repr(dt))
    sleep(1)
    
    # Test the forward method
    print("Testing forward method")
    dt.forward(100)
    dt.print_state()
    sleep(2)
    
    # Test the backward method
    print("Testing backward method")
    dt.backward(100)
    dt.print_state()
    sleep(2)
    
    # Test the turn_left method
    print("Testing turn_left method")
    dt.turn_left(100)
    dt.print_state()
    sleep(2)
    
    # Test the turn_right method
    print("Testing turn_right method")
    dt.turn_right(100)
    dt.print_state()
    sleep(2)
    
    # Test the stop method
    print("Testing stop method")
    dt.stop()
    dt.print_state()
    sleep(2)
    
    # Test the move method
    print("Testing move method")
    dt.move(100, 100)
    dt.print_state()
    sleep(2)
    
    print("Testing stop method")
    dt.stop()
    dt.print_state()
    sleep(2)
    
    print("Test swerve left")
    dt.move(75, 100)
    dt.print_state()
    sleep(2)
    
    print("Test swerve right")
    dt.move(100, 75)
    dt.print_state()
    sleep(2)
    
    dt.stop()
    
    print("Test complete")
        
# Test the DriveTrain class
if __name__ == "__main__":
    run_tests_4()