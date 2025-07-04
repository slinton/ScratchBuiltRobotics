#
# PWMServoMotor
#
# Version: 1.00
# Date: 2025-07-01
# Author: Sam Linton
# Description: ServoMotor controlled directly via PWM signals from the Pico
#
#
from time import sleep
from machine import Pin, PWM
from typing import override
from servo_motor import ServoMotor


class PWMServoMotor(ServoMotor):
    def __init__(self, 
                 name: str = '',
                 pin: int = 0,
                 raw_angle_0: float = 0.0,
                 angle_start: float = 0.0,
                 angle_end: float = 180.0,
                 angle_home: float = 90.0,
                 min_us: float = 544.0,
                 max_us: float = 2400.0,
                 freq: int = 50
                 ) -> None:
        super().__init__(name, pin, raw_angle_0, angle_start, angle_end, angle_home, min_us, max_us, freq)
        self._pwm: PWM  = PWM(Pin(pin))
        self._pwm.freq(freq) 
    
    @override
    def off(self) -> None:
        """Turn off the servo by setting duty cycle to 0."""
        self._pwm.duty_ns(0)

    @override
    def _write_raw_angle(self, raw_angle: float) -> None:
        """Write the raw angle to the servo."""
        us = self._min_us + (raw_angle / 180.0) * (self._max_us - self._min_us)
        self._pwm.duty_ns(int(us * 1000.0))

    @override
    def _sleep(self, seconds: float) -> None:
        """Sleep for a given number of seconds."""
        sleep(seconds)  

if __name__ == '__main__':
    # Create a PWMServoMotor instance
    servo = PWMServoMotor(name='TestServo',  pin=1)
    print(servo)

    # Home the servo
    print('Homing servo...', end='')
    servo.home(time=1.0)
    print('Done.')

    # Test move_to
    print(f'Moving to 170 degrees...', end='')
    servo.move_to_angle(170.0, time=1.0)
    print('Done.')
    print(f'Moving to 10 degrees...', end='')
    servo.move_to_angle(10.0, time=1.0)
    print('Done.')

    # Turn off the servo
    print('Turning off servo...', end='')
    servo.off()
    print('Done.')