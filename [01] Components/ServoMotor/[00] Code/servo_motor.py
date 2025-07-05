#
# ServoMotor
#
# Version: 1.00
# Date: 2025-07-01
# Author: Sam Linton
# Description: Control of servo motor 
#
# Note: This will replace Servo, ServoInfo, and ServoBase
#
# raw = sign * angle + raw_angle_0
# angle = sign * (raw - raw_angle_0)
#
# TODO: Maybe have modes SPEED_CONTROL, ANGLE_CONTROL
#

import uasyncio as asyncio

class ServoMotor:
    STOPPED: str = 'stopped'
    INCREASING: str = 'increasing'
    DECREASING: str = 'decreasing'
    MAX_ANGLE_DEG: float = 180.0
    ANGLE_INC: float = 2.0
    MIN_US: float = 544.0 # Or 600.0
    MAX_US: float = 2400.0
    FREQ: int = 50 # PWM frequency in Hz
    
    def __init__(self, 
                 name: str ='',
                 pin: int = 0,
                 raw_angle_0: float = 0.0, # Raw angle corresponding to angle = 0.0
                 angle_start: float = 0.0, # Logical starting angle
                 angle_end: float = 180.0, # Logical ending value
                 angle_home: float = 90.0, # Logical home angle
                 ) -> None:
        self._name: str = f'Servo: {str(pin)}' if name == '' else name
        self._pin: int = pin 

        self._initialized: bool = False # angle is not initialized
        self._angle: float = angle_home
        self._raw_angle_0: float = raw_angle_0
        self._sign: int = 1 if angle_end > angle_start else -1

        self._angle_start: float = angle_start
        self._angle_end: float = angle_end
        self._angle_home: float = angle_home

        self._state = ServoMotor.STOPPED

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def pin(self) -> int:
        return self._pin
    
    @property
    def angle(self) -> float:
        if not self._initialized:
            raise ValueError("Angle not initialized.")
        return self._angle
    
    def write_angle(self, angle: float) -> None:
        """Write logical angle to the servo."""
        raw_angle = self._raw_angle_from_angle(angle)
        if not self.angle_in_range(angle):
            raise ValueError(f'Angle {angle} is out of range ({self._angle_start}, {self._angle_end})')
        self._write_raw_angle(raw_angle)
        self._angle = angle
        self._initialized = True
    
    def _write_raw_angle(self, raw_angle: float) -> None:
        """Write the servo angle to the hardware."""
        raise NotImplementedError("This method should be overridden in subclasses.")
    
    # TODO: Add an async version of this method
    def move_to_angle(self, angle: float, time: float = 0.0, angle_inc: float = 1.0) -> None:
        start_angle = self._angle
        num_steps: int = int(abs((angle - start_angle) / angle_inc)) # Counts now 
        
        # Immediate move if no time
        if time <= 0.0 or num_steps <= 1:
            self.write_angle(angle)
            return
        
        # Move in steps
        angle_inc = (angle - start_angle) / num_steps
        time_inc = time / (num_steps - 1)
        
        t = 0.0
        for n in range(num_steps):
            new_angle: float = start_angle + (n + 1) * angle_inc
            print(f'Moving to angle: {new_angle} (step {n}/{num_steps})')
            self.write_angle(new_angle)
            if n < num_steps -1: 
                self._sleep(time_inc)
                t += time_inc
            print(f'Angle {new_angle} at time {t:.2f} seconds')

    def move_by(self, angle_inc: float) -> None:
        if not self._initialized:
            raise ValueError('Servo angle not initialized. Please set the angle first.')
        
        new_angle = self._angle + angle_inc
        if self.angle_in_range(new_angle):
            self.write_angle(new_angle)

    def home(self, time: float = 0.0, angle_inc: float = 1.0) -> None:
        """Move to the home angle."""
        self.move_to_angle(self._angle_home, time=time, angle_inc=angle_inc)

    def move_to_start(self, time: float = 0.0, angle_inc: float = 1.0) -> None:
        """Move to the start angle."""
        self.move_to_angle(self._angle_start, time=time, angle_inc=angle_inc)

    def move_to_end(self, time: float = 0.0, angle_inc: float = 1.0) -> None:
        """Move to the end angle."""
        self.move_to_angle(self._angle_end, time=time, angle_inc=angle_inc)

    def start_increasing(self) -> None:
        if not self._state == ServoMotor.INCREASING:
            print('start_increasing')
        self._state = ServoMotor.INCREASING

    def start_decreasing(self) -> None:
        if not self._state == ServoMotor.DECREASING:
            print('start_decreasing')
        self._state = ServoMotor.DECREASING

    def stop(self) -> None:
        if not self._state == ServoMotor.STOPPED:
            print('stop')
        self._state = ServoMotor.STOPPED

    def off(self) -> None:
        pass

    def _sleep(self, seconds: float) -> None:
        pass
    
    def angle_in_range(self, angle: float) -> bool:
        """True if the logical angle is within the allowed range."""
        return  (self._angle_end - angle) * (angle - self._angle_start) >= 0.0
    
    def _raw_angle_from_angle(self, angle: float) -> float:
        """Get the servo angle from the logical angle"""
        return self._raw_angle_0 + self._sign * angle
    
    def _angle_from_raw_angle(self, raw_angle: float) -> float:
        return self._sign * (raw_angle - self._raw_angle_0)
    
    def __str__(self) -> str:
        return f'{self._name} at pin {self._pin}\n' + \
            f'Angle: {self._angle}\n' + \
            f'Angle Range: {self._angle_start}-{self._angle_end}\n' + \
            f'Home Angle: {self._angle_home}\n' + \
            f'Zero Raw Angle = {self._raw_angle_0}'
    
    # TODO: Do I need a special mode for this? Maybe a better name?
    async def run_loop(self, angle_inc: float = ANGLE_INC) -> None:
        while True:
            try:
                while self._state == ServoMotor.INCREASING:
                    self.move_by(self._sign * angle_inc)
                    await asyncio.sleep_ms(10)

                while self._state == ServoMotor.DECREASING:
                    self.move_by(-self._sign * angle_inc)
                    await asyncio.sleep_ms(10)

                if self._state == ServoMotor.STOPPED:
                    await asyncio.sleep_ms(10)
                    
            except Exception as e:
                print(f'Exception: {e}')
                self._state = ServoMotor.STOPPED
    
   
if __name__ == "__main__":
    # Test code
    servo_motor = ServoMotor(pin=2, angle_start=0, angle_end=180, name='Servo 2')
    print(servo_motor)

