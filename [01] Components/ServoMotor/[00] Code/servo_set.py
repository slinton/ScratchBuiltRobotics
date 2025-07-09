#
# ServoSet
#
# Version: 1.00
# Date: 2025-07-07
# Author: Sam Linton
# Description: Represents a set of servos
# 
#
#
from servo_motor import ServoMotor
from position import Position
from time import sleep
import math


class ServoSet:
    def __init__(self, servos: list[ServoMotor]) -> None:
        self.servos = servos

    # Make this async, or just a loop?
    def move_to_position(self, position: Position, time: float = 0.0, num_steps: int = 10) -> None:

        # Check for number of servos and position angles match
        if len(position.angles) != len(self.servos):
            raise ValueError("Position and servo count mismatch")
        
        # Check if all angles are in range for the servos
        if  not all(servo.angle_in_range(angle) for servo, angle in zip(self.servos, position.angles)):
            raise ValueError("Position angles out of range for servos")
        
        # If no time or steps, set angles immediately
        if num_steps <= 1 or time <= 0.0:
            for i, servo in enumerate(self.servos):
                servo.set_angle(position[i])
            return
        
        # Get angle increments for each servo
        angle_inc: list[float] = []
        for i, servo in enumerate(self.servos):
            angle_inc[i] = (position[i] - servo.angle)/num_steps

        # Loop through the number of steps
        for _ in range(num_steps):
            # Update each servo angle
            for i, servo in enumerate(self.servos):
                new_angle = servo.angle + angle_inc[i]
                servo.set_angle(new_angle)
            print(f"Moving to position: {[servo.angle for servo in self.servos]} (step {_ + 1}/{num_steps})")
            sleep(time / num_steps)

    def _get_delta_angle(self, position: Position) -> float:
        """Calculate the magnitude of the change in angle from the current angles to the target angles."""
        return math.sqrt(sum((position[i] - servo.angle) ** 2 for i, servo in enumerate(self.servos)))
        
            

if __name__ == "__main__":
    # Example usage
    servo1 = ServoMotor(name="Servo 1", pin=17, angle_start=0.0, angle_end=180.0, angle_home=90.0)
    servo2 = ServoMotor(name="Servo 2", pin=18, angle_start=0.0, angle_end=180.0, angle_home=90.0)
    
    servo_set = ServoSet(servos=[servo1, servo2])
    
    position = Position(angles=[45.0, 135.0], name="Test Position")
    
    servo_set.move_to_position(position, time=2.0, num_steps=10)