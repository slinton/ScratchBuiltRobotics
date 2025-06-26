#
# Lifter
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: A class that runs the lifter mechanism of a claw.
#
from time import sleep
from servo_base import ServoBase


class Lifter(ServoBase):
    """Implement a lifter mechanism"""
     
    def __init__(self,
                 pin: int=16,
                 servo_top_angle: float = 0.0,
                 servo_bottom_angle: float = 180.0,
                 ) -> None:
        """Initializer

        Args:
            pin (int, optional): pin for the lifter PWM signal. Defaults to 16.
            servo_top_angle (float, optional): Angle in degrees corresponding to lifter at top of. Defaults to 0.0.
            servo_bottom_angle (float, optional): Angle in degrees corresponding to lifter at bottom. Defaults to 180.0.
        """
        super().__init__(pin, servo_top_angle, servo_bottom_angle)
        
    def start_lift(self) -> None:
        self.start_decreasing()
        
    def start_lower(self) -> None:
        self.start_increasing()
        
    def lift(self, time: float = None) -> None:
        """Move gripper to the top
        """
        self.move_to_start()
        
    def lower(self, time: float = None) -> None:
        """Move gripper to the bottom
        """
        self.move_to_end()
        

if __name__ == '__main__':
    lifter = Lifter()
    lifter.lift()
    sleep(0.5)
    lifter.lower()
    sleep(0.5)
    lifter.lift()