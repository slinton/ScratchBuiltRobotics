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
#       reset and set FREQuency
#
import ustruct
from time import sleep
# from typing import override
from machine import I2C
from servo_controller import ServoController
from servo_motor import ServoMotor


class I2CServoMotor(ServoMotor):
    ADDRESS: int = 0x40  # Default I2C address for PCA9685

    def __init__(self, 
                 pin: int,
                 servo_controller: ServoController,
                 name: str = '',
                 raw_angle_0: float = 0.0,
                 sign: int = 1,  # 1 for increasing angle, -1 for decreasing angle
                 angle_start: float = 0.0,
                 angle_end: float = 180.0,
                 angle_home: float = 90.0,
                 ) -> None:
        super().__init__(name, pin, raw_angle_0, sign, angle_start, angle_end, angle_home)

        self._i2c: I2C = servo_controller.i2c

    # @override
    def _set_raw_angle(self, raw_angle: float) -> None:
        duty = self._raw_angle_to_duty(raw_angle)
        address = 0x06 + 4 * self._pin
        
        # Create data to write to I2C
        data = ustruct.pack('<HH', 0, duty) 
        self._i2c.writeto_mem(I2CServoMotor.ADDRESS, address,  data) 

    # @override
    def _sleep(self, seconds: float) -> None:
        """Sleep for a given number of seconds."""
        sleep(seconds)
        
    # @override
    def off(self) -> None:
        address = 0x06 + 4 * self._pin
        
        # Create data to write to I2C
        data = ustruct.pack('<HH', 0, 0) # type: ignore
        self._i2c.writeto_mem(I2CServoMotor.ADDRESS, address,  data)

    # TODO: how does this compare to the PWM case?
    def _raw_angle_to_duty(self, raw_angle: float) -> int:
        """Convert raw angle to duty cycle."""
        t_period_us: int = int(1_000_000 / ServoMotor.FREQ) # period in us
        min_duty: float = self._us2duty(ServoMotor.MIN_US, t_period_us)
        max_duty: float = self._us2duty(ServoMotor.MAX_US, t_period_us)

        slope: float = (max_duty - min_duty) / ServoMotor.MAX_ANGLE_DEG
        
        return int(min_duty + slope * raw_angle)

    def _us2duty(self, us: float, t_period_us: float) -> int:
        """Convert microseconds to duty cycle."""
        return int((us / t_period_us) * 4096)
    

if __name__ == "__main__":
    # Test code
    from machine import Pin
    from servo_controller import ServoController

    i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # Adjust pins as necessary
    servo_controller = ServoController(i2c)
    
    servo = I2CServoMotor(pin=0, servo_controller = servo_controller)
    print(servo)

    try:
        print('Write angle to 10...', end='')
        servo.set_angle(10)
        print('done')
        sleep(1)
        
        print('Write angle to 170...', end='')
        servo.set_angle(170)
        print('done')
        sleep(1)
        
        print('Move to angle to 10...', end='')
        servo.move_to_angle(10, time=2)  # Move to 180 degrees over 2 seconds
        print('done')
        sleep(1)
        
        print('Turning off servo...', end='')
        servo.off()
        print('Done.')
        sleep(5)
        
    except Exception as e:
        print(f"Error: {e}")