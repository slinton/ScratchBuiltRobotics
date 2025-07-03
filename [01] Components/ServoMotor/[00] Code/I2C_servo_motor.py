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
    def __init__(self, 
                 pin: int,
                 i2c: I2C,
                 address: int = 0x40,
                 name: str = '',
                 raw_angle_0: float = 0.0,
                 angle_start: float = 0.0,
                 angle_end: float = 180.0,
                 angle_home: float = 90.0,
                 min_us: float = 544.0,
                 max_us: float = 2400.0,
                 freq: int = 50
                 ) -> None:
        super().__init__(name, pin, raw_angle_0, angle_start, angle_end, angle_home, min_us, max_us, freq)

        self._i2c: I2C = i2c
        self._address: int = address



    @override
    def _read_raw_angle(self) -> float:
        """Read the raw angle from the servo."""
        raise NotImplementedError("I2CServoMotor does not implement _read_raw_angle")

    @override
    def _write_raw_angle(self, raw_angle: float) -> None:
        """Write the raw angle to the servo."""
        raise NotImplementedError("I2CServoMotor does not implement _write_raw_angle")

    @override
    def _sleep(self, seconds: float) -> None:
        """Sleep for a given number of seconds."""
        sleep(seconds)  