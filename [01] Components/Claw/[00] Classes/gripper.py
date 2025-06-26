#
# Gripper
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
#
# Description: A class that runs the gripper mechanism of a claw.
#
from time import sleep
from servo_base import ServoBase

class Gripper(ServoBase):
    """Implement gripper mechanism"""
    
    def __init__(self, pin: int=17, servo_close_angle: float = 70.0, servo_open_angle: float=160.0) -> None:
        """Initializer

        Gripper angle goes from 0 (closed) to open_angle (fully open)
        These angles correspond with the servo_close_angle and servo_open_angle, respectively

        Args:
            pin (int, optional): pin for the gripper PWM signal. Defaults to 16.
            open_angle (float, optional): Angle in degrees corresponding to open gripper. Defaults to 160.0.
            close_angle (float, optional): Angle in degrees corresponding to closed gripper. Defaults to 70.0.
        """
        super().__init__(pin, angle_start=servo_close_angle, angle_end=servo_open_angle)
        
    def open(self, time:float = None) -> None:
        """Open the gripper completely
        """
        self.move_to_end()
        
    def close(self, time: float = None) -> None:
        """Close the gripper completely
        """
        self.move_to_start()
            
    def start_open(self) -> None:
        self.start_increasing()
  
    def start_close(self) -> None:
        self.start_decreasing()
        
        
if __name__ == '__main__':
    gripper = Gripper()
    print('Closing...', end='')
    gripper.close()
    print('closed')
    sleep(1)
    
    print('Opening...', end='')
    gripper.open()
    print('open')
    sleep(1)
    
    print('Closing...', end='')
    gripper.close()
    print('closed')
    sleep(1)

    print('Moving to 160...', end='')
    gripper.move_to_angle(160, 1)
    print('moved')
        
    print('Moving to 70...', end='')
    gripper.move_to_angle(70, 1)
    print('moved')
