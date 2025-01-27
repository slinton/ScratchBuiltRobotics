#
# ServoSet
#
import ustruct
from math import radians
from typing import Tuple, List
from machine import I2C
from time import sleep
from servo_info import ServoInfo

class ServoSet:
    """Uses the PCA9685 to control a set of servos.
    """

    def __init__(self, 
                 i2c: I2C, 
                 servo_infos: List[ServoInfo], 
                 address: int = 0x40, 
                 freq: int = 50, 
                 min_us: int = 600, 
                 max_us: int = 2400,
                 max_angle_deg: float = 180) -> None:
        """_summary_

        Args:
            i2c I2C: I2C object
            servo_infos (List[ServoInfo]): list of servo info objects
        """
        self._i2c = i2c
        self._servo_infos = servo_infos
        self._address = address

        # Compute min and max duty cycles (0-4095)
        t_period_us: int = 1_000_000 / freq # period in us
        min_duty: int = self._us2duty(min_us, t_period_us)
        max_duty: int = self._us2duty(max_us, t_period_us)

        # Slope and offset for converting angles (degrees) to duty cycles [0, 4095]
        self._slope = (max_duty - min_duty) / max_angle_deg
        self._offset = min_duty

        self.reset()

    def _us2duty(self, t_us: int, t_period_us: float) -> int:
        return int(4095 * t_us / t_period_us)

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
        return angle

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

    def _angle_to_duty(self, angle_deg: float) -> int:
        """Convert the angle to a duty cycle

        Args:
            angle_deg (float): angle in deg to convert to a duty cycle

        Returns:
            int: duty cycle [0, 4095]
        """
        return int(self._offset + self._slope * angle_deg)

    def _duty_to_angle(self, duty: int) -> float:
        """Convert the duty cycle to an angle

        Args:
            duty (int): duty cycle [0, 4095] to convert to an angle

        Returns:
            float: angle in deg
        """
        return float(duty - self._offset) / self._slope
    

if __name__ == "__main__":
    # Test code
    from servo_info import ServoInfo
    from machine import I2C

    # Create I2C object
    i2c = I2C(0, sda=0, scl=1)

    # Create servo info objects
    servo_infos = [ServoInfo(0, 0, 180), ServoInfo(1, 0, 180)]

    # Create ServoSet object
    servo_set = ServoSet(i2c, servo_infos)

    # Move servos to angles
    servo_set.move_to_angle([(0, 170), (1, 170)], time=1, num_steps=100)
    servo_set.move_to_angle([(0, 10), (1, 10)], time=1, num_steps=100)