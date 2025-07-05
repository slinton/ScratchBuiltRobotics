#
# I2CServoMotor
#
# Version: 1.00
# Date: 2025-07-01
# Author: Sam Linton
# Description: ServoMotor controlled using PCA9685 I2C servo controller
#
# TODO: perhaps have an external PCA9685 class that handles the I2C communication,
#       and this class just uses that to set the angle. That way, PCA9685 can do its own
#       reset and set frequency
#
from time import sleep
from typing import override
from machine import I2C
from servo_motor import ServoMotor


class I2CServoMotor(ServoMotor):
    ADDRESS: int = 0x40  # Default I2C address for PCA9685

    def __init__(self, 
                 pin: int,
                 i2c: I2C,
                 name: str = '',
                 raw_angle_0: float = 0.0,
                 angle_start: float = 0.0,
                 angle_end: float = 180.0,
                 angle_home: float = 90.0,
                 ) -> None:
        super().__init__(name, pin, raw_angle_0, angle_start, angle_end, angle_home)

        self._i2c: I2C = i2c

    @override
    def _write_raw_angle(self, raw_angle: float) -> None:
        duty = self._servo_angle_to_duty(servo_angle)
        address = 0x06 + 4 * self._pin
        
        # Create data to write to I2C
        data = ustruct.pack('<HH', 0, duty) # type: ignore
        self._i2c.writeto_mem(self._address, address,  data) # type: ignore

    @override
    def _sleep(self, seconds: float) -> None:
        """Sleep for a given number of seconds."""
        sleep(seconds)  