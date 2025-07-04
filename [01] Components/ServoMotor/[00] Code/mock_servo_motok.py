#
# MockServoMotor
#
# Version: 1.00
# Date: 2025-07-01
# Author: Sam Linton
# Description: Mock implementation of ServoMotor for testing purposes.
#
#
from typing import override
from servo_motor import ServoMotor

class MockServoMotor(ServoMotor):
    """Mock implementation of ServoMotor for testing purposes."""
    
    def __init__(self, 
                 name: str = 'MockServoMotor',
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
        self._angle = angle_home  # Initialize to home position

    @override
    def _write_raw_angle(self, raw_angle: float) -> None:
        print(f"[Mock] Writing raw angle: {raw_angle}")

    @override
    def _sleep(self, seconds: float) -> None:
        import time
        print(f"[Mock] Sleeping for {seconds} seconds")
        time.sleep(seconds)


if __name__ == '__main__':
    # Example usage
    servo = MockServoMotor(
        name='TestServo', 
        pin=1, 
        raw_angle_0=90.0, 
        angle_start=-45.0, 
        angle_end=45.0,
        angle_home=0.0)
    
    try:
        print(servo.angle)
    except ValueError as e:
        print(f'Error: {e}')
    
    print(f'{servo}\n')

    print('\nTest write and read angle:')
    angle = -30.0
    print(f'write_angle: {angle}')
    servo.write_angle(angle)
    print(f'Angle after write: {servo.angle}')

    print('\nTest move to angle:')
    new_angle = 30.0
    print(f'Moving to angle: {new_angle}')
    servo.move_to_angle(new_angle, time=6.0, angle_inc=10)
    print(f'Angle after move: {servo.angle}')