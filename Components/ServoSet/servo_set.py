#
# ServoSet
#
import ustruct
from typing import Tuple, List
from machine import I2C
from time import sleep
from servo_info import ServoInfo

class ServoSet:
    """Uses the PCA9685 to control a set of servos.
    """

    def __init__(self, i2c: I2C, servo_infos: List[ServoInfo]) -> None:
        """_summary_

        Args:
            i2c I2C: I2C object
            servo_infos (List[ServoInfo]): list of servo info objects
        """
        self._i2c = i2c
        self._servo_infos = servo_infos
        self._address = 0x40
        self.reset()

    def reset(self) -> None:
        self._write(0x00, 0x00) # Mode1

    def write(self, index: int, angle: float) -> None:
        """Write the angle to the servo

        Args:
            index (int): index of the servo
            angle (float): angle to write to the servo
        """
        # Find duty cycle from angle
        duty = self._angle_to_duty(angle)
        
        # Create data to write to I2C
        data = ustruct.pack('<HH', 0, duty)
        self.i2c.writeto_mem(self.address, 0x06 + 4 * index,  data)


    def read(self, index: int) -> float:
        # TODO: Check this
        """Read the angle from the servo

        Args:
            index (int): index of the servo

        Returns:
            float: angle of the servo
        """
        # Read the duty cycle from the servo
        data = self.i2c.readfrom_mem(self.address, 0x06 + 4 * index, 1)[0]
        duty = ustruct.unpack('<HH', data)
        angle = self._duty_to_angle(duty)


    def move_to_angle(self, servo_angles: Tuple[int, float], time: float | None = None, num_steps: int = 100) -> None:
        """Move to the given angle in the given time (seconds)

        Args:
            servo_info (Tuple[int, float]): servo index and angle to move to (deg)
            time (float): time (in seconds) to move between angles
            num_steps (int): number of steps to take in the movement
        """ 
        # Loop over all requested angle values
        for index, angle in servo_angles:
            servo_info = self._servo_infos[index]

            # Check to make sure the new_angle is within the limits
            if not servo_info.angle_in_range(angle):
                raise ValueError('new_angle is not within the range of the servo')
            
            # Retrieve current angle
            current_angle = self.read(index)

            # Move in a single step to the new angle
            angle_inc: float = angle - current_angle
            time_inc: float = time / (num_steps - 1)
            for i in range(num_steps):
                angle: float = current_angle + i * angle_inc
                self.write(index, angle)
                sleep(time_inc)


    def _angle_to_duty(self, angle: float) -> int:
        """Convert the angle to a duty cycle

        Args:
            angle (float): angle to convert to a duty cycle

        Returns:
            int: duty cycle
        """
        pass 

    def _duty_to_angle(self, duty: int) -> float:
        """Convert the duty cycle to an angle

        Args:
            duty (int): duty cycle to convert to an angle

        Returns:
            float: angle
        """
        pass