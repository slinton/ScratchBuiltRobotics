#
# ServoSet
#
# Version: 1.00
# Date: 2025-07-07
# Author: Sam Linton
# Description: Represents a set of servos
#
# TODO:
# Read from a file
# get_home_position -> position that holds homes
# same for start, end
# Fix irritating issue when out of range 
#
#
#
#
from servo_motor import ServoMotor
from movement import Movement
from position import Position
from time import sleep
import math


class ServoSet:
    def __init__(self, servos: list[ServoMotor], name: str = '') -> None:
        self._name = name
        self._servos = servos

    @property
    def name(self) -> str:
        return self._name

    def get_home_position(self) -> Position:
        """Get the home position of the servo set."""
        angles: list[float] = [servo.angle_home for servo in self._servos]
        return Position(angles=angles, name=f"{self._name} Home Position")
    
    def get_start_position(self) -> Position:
        """Get the start position of the servo set."""
        angles: list[float] = [servo.angle_start for servo in self._servos]
        return Position(angles=angles, name=f"{self._name} Start Position")
    
    def get_end_position(self) -> Position:
        """Get the end position of the servo set."""
        angles: list[float] = [servo.angle_end for servo in self._servos]
        return Position(angles=angles, name=f"{self._name} End Position")

    # Make this async, or just a loop?
    def move_to_position(self, position: Position, time: float = 0.0, num_steps: int = 10) -> None:

        # Check for number of servos and position angles match
        if len(position.angles) != len(self._servos):
            raise ValueError("Position and servo count mismatch")
        
        # Check if all angles are in range for the servos
        if  not all(servo.angle_in_range(angle) for servo, angle in zip(self._servos, position.angles)):
            raise ValueError("Position angles out of range for servos")
        
        # If no time or steps, set angles immediately
        if num_steps <= 1 or time <= 0.0:
            for i, servo in enumerate(self._servos):
                servo.set_angle(position[i])
            return
        
        # Get angle increments for each servo
        angle_inc: list[float] = []
        for i, servo in enumerate(self._servos):
            angle_inc.append((position[i] - servo.angle)/num_steps)

        # Loop through the number of steps
        for _ in range(num_steps):
            # Update each servo angle
            for i, servo in enumerate(self._servos):
                new_angle = servo.angle + angle_inc[i]
                servo.set_angle(new_angle)
            print(f"Moving to position: {[servo.angle for servo in self._servos]} (step {_ + 1}/{num_steps})")
            sleep(time / num_steps)
            
    def get_angles(self) -> list[float]:
        return [servo.angle for servo in self._servos]
        
    def set_angles(self, angles: list[float]) -> None:
        for i, angle in enumerate(angles):
            self._servos[i].set_angle(angle)
            
    def home(self) -> None:
        for servo in self._servos:
            servo.home()
            
    def execute_movement(self, movement: Movement) -> None:
        for n in range(movement.num_positions):
            time, position = movement[n]
            self.move_to_position(position, time=time, num_steps=100)

    def _get_delta_angle(self, position: Position) -> float:
        """Calculate the magnitude of the change in angle from the current angles to the target angles."""
        return math.sqrt(sum((position[i] - servo.angle) ** 2 for i, servo in enumerate(self._servos)))
    
    def __str__(self) -> str:
        return f'{self._name}: {self.get_angles()}'
        
            
if __name__ == "__main__":
    from machine import I2C, Pin
    from servo_controller import ServoController
    from i2c_servo_motor import I2CServoMotor
    
    # Create i2c
    i2c = I2C(id=1, sda=Pin(14), scl=Pin(15))
    devices = i2c.scan()
    if len(devices) > 0:
        print(f'Found {len(devices)} devices on I2C {id}:')
        for device in devices:  
            print(f'\tDecimal address: {device}  Hex address: {hex(device)}')
    else:
        print(f'Found no devices on I2C:')
           
    # Create servo controller
    sc = ServoController(i2c = i2c)

    # Create servos and servoset
    servos: list[ServoMotor] = [
        I2CServoMotor(
            name='lower-leg', 
            pin = 1, 
            servo_controller = sc, 
            raw_angle_0 = 70, 
            angle_start=0, 
            angle_end=110, 
            angle_home=90),
        I2CServoMotor(
            name='shoulder-forward', 
            pin = 2, 
            servo_controller = sc, 
            raw_angle_0 = 70, 
            angle_start=0, 
            angle_end=90, 
            angle_home=45),
                I2CServoMotor(
            name='shoulder-out',  
            pin = 3, 
            servo_controller = sc, 
            raw_angle_0 = 80, 
            angle_start=-30, 
            angle_end=30, 
            angle_home=0)
    ]
    
    # Create servo set
    servo_set = ServoSet(servos=servos, name = 'test')
    
    # Home
    servo_set.home()
    home_position = servo_set.get_home_position()
    print(servo_set)

    # Get start and end positions
    start_position = servo_set.get_start_position()
    end_position = servo_set.get_end_position()
    servo_set.move_to_position(start_position, time=2.0, num_steps=100)
    print(f'Start Position: {start_position}')
    servo_set.move_to_position(end_position, time=2.0, num_steps=100)
    print(f'End Position: {end_position}')
    
    # Create position
    position = Position(angles=[110.0, 70.0, 0.0], name="Test Position")
    
    servo_set.move_to_position(position, time=2.0, num_steps=100)