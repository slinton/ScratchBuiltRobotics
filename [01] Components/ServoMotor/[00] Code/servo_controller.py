#
# ServoController 
#
# Version: 1.00
# Date: 2025-07-03
# Author: Sam Linton
# Description: PCA89685 I2C servo controller
#
#
# raw = sign * angle + raw_angle_0
# angle = sign * (raw - raw_angle_0)
#
#
from machine import I2C
from time import sleep_us


class ServoController:
    ADDRESS: int = 0x40  # Default I2C address for PCA9685
    MIN_US: float = 544.0  # Minimum pulse width in microseconds
    MAX_US: float = 2400.0  # Maximum pulse width in microseconds
    FREQ: int = 50  # PWM frequency in Hz

    def __init__(self, i2c: I2C) -> None:
        """Initialize the servo controller with the given I2C interface."""
        self._i2c = i2c
        self.reset()
        self.set_freq(ServoController.FREQ)

    def reset(self) -> None:
        self._write(0x00, 0x00) # Mode1

    def set_freq(self, freq: int) -> None:
        prescale: int = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode: int = self._read(0x00) # Mode 1
        self._write(0x00, (old_mode & 0x7F) | 0x10) # Mode 1, sleep
        self._write(0xfe, prescale) # Prescale
        self._write(0x00, old_mode) # Mode 1
        sleep_us(5)
        self._write(0x00, old_mode | 0xa1) # Mode 1, autoincrement on

    def _write(self, address: int, value: int) -> None:
        self._i2c.writeto_mem(ServoController.ADDRESS, address, bytearray([value])) # type: ignore

    def _read(self, address: int) -> int:
        return self._i2c.readfrom_mem(self._address, address, 1)[0] # type: ignore
    
   
if __name__ == "__main__":
    # Test code
    pass

