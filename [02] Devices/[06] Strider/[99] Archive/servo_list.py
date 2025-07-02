#
# ServoList
#
# Version: 1.00
# Date: 2025-06-10
# Author: Sam Linton
# Description: Represents a set of servos controlled by a PCA9685 I2C servo controller.
#
# TODO: 
# - use actual time for movement, not just sleep.
# - perhaps make multiple move method use entire array, not just specified indices.
# - can't execute_gesture be derived from async_execute_gesture?
#
import ustruct # type: ignore
from machine import I2C, Pin # type: ignore
from time import sleep, sleep_us, ticks_us # type: ignore
import uasyncio as asyncio # type: ignore
from servo_info import ServoInfo
from gesture import Gesture

class ServoList:
    """Uses the PCA9685 to control a set of servos.
    In this class, "angle" refers to the logical angle of the servo, which is a value that is
    determined by the application. The physical angle of the servo is referred to as "servo_angle".
    """
    def __init__(self, 
                 i2c: I2C, # type: ignore
                 servo_infos: list[ServoInfo],
                 address: int = 0x40, 
                 freq: float = 50, 
                 min_us: float = 600.0, # 544
                 max_us: float = 2400.0,
                 max_angle_deg: float = 180.0) -> None:
        """constructor

        Args:
            i2c I2C: I2C object
            servo_infos (List[ServoInfo]): list of servo info objects
        """
        self._i2c: I2C = i2c
        self._servo_infos: list[ServoInfo] = servo_infos
        self._address: int = address

        # Compute min and max duty cycles (0-4095)
        t_period_us: int = int(1_000_000 / freq) # period in us
        min_duty: float = self._us2duty(min_us, t_period_us)
        max_duty: float = self._us2duty(max_us, t_period_us)

        # Slope and offset for converting servo angles (degrees) to duty cycles [0, 4095]
        self._slope: float = (max_duty - min_duty) / max_angle_deg
        self._offset: float = min_duty
        
        print('resetting...', end='')
        self.reset()
        print('done')
        self.set_freq(freq)
        
        # Set all servo angles
        for servo_info in self._servo_infos:
            servo_angle: float = self.read(servo_info.index)
            servo_info.angle = servo_info.get_angle(servo_angle)
            
    def _us2duty(self, t_us: float, t_period_us: float) -> int:
        return int(4095 * t_us / t_period_us)

    def reset(self) -> None:
        self._write(0x00, 0x00) # Mode1
        
    def set_freq(self, freq: float):
        prescale: int = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode: int = self._read(0x00) # Mode 1
        self._write(0x00, (old_mode & 0x7F) | 0x10) # Mode 1, sleep
        self._write(0xfe, prescale) # Prescale
        self._write(0x00, old_mode) # Mode 1
        sleep_us(5)
        self._write(0x00, old_mode | 0xa1) # Mode 1, autoincrement on
        
    def _write(self, address: int, value: int) -> None:
        """Write value to the I2C address

        Args:
            address (int): I2C address
            value (int): value
        """
        self._i2c.writeto_mem(self._address, address, bytearray([value])) # type: ignore

    def _read(self, address: int) -> int:
        """Read value from the I2C address

        Args:
            address (int): I2C address

        Returns:
            int: value read from the address
        """
        return self._i2c.readfrom_mem(self._address, address, 1)[0] # type: ignore
        
    def write(self, index: int, angle: float) -> None:
        """Move the servo with the given index to the specified logical angle

        Args:
            index (int): index of the servo
            angle (float): logical angle in degrees to write to the servo
        """
        servo_info: ServoInfo = self._servo_infos[index]
        if not servo_info.angle_in_range(angle):
            raise ValueError(f'Angle {angle} is out of range for servo {index}: {servo_info}.')
        
        # Find duty cycle from angle
        servo_angle: float = servo_info.get_servo_angle(angle)
        #print(f'write to angle {angle} servo angle {servo_angle}')
        duty = self._servo_angle_to_duty(servo_angle)
        #address = 0x06 + 4 * index
        address = 0x06 + 4 * servo_info.pin
        
        # Create data to write to I2C
        data = ustruct.pack('<HH', 0, duty) # type: ignore
        self._i2c.writeto_mem(self._address, address,  data) # type: ignore

    def read(self, index: int) -> float:
        """Read the logical angle from the servo with the given index

        Args:
            index (int): index of the servo

        Returns:
            float: angle of the servo
        """
        # Read the duty cycle from the servo
        servo_info: ServoInfo = self._servo_infos[index]
        address = 0x06 + 4 * servo_info.pin
        #address = 0x06 + 4 * index
        data = self._i2c.readfrom_mem(self._address, address, 4) 
        duty: int = ustruct.unpack('<HH', data)[1]
        servo_angle = self._duty_to_servo_angle(duty)
        angle = self._servo_infos[index].get_angle(servo_angle)
        return angle

    def move_to_angle(self, index: int, angle: float, time: float | None = None, num_steps: int | None = None) -> None:
        """Move the specified servo to the given logical angle in the given time (seconds)

        Args:
            index (int) servo index
            angle (float) logical angle to move to in degrees
            time (float): time (in seconds) to move between angles
            num_steps (int): number of steps to take in the movement
        """ 
        # Current servo
        servo_info = self._servo_infos[index]

        # Check to make sure the new_angle is within the limits
        if not servo_info.angle_in_range(angle):
            raise ValueError('new_angle is not within the range of the servo')
            
        # Retrieve current angle
        current_servo_angle = self.read(index)
        current_angle = servo_info.get_angle(current_servo_angle)
        
        if num_steps is None:
            num_steps = abs(int(angle - current_angle)) # 1 degree per step 

        # Incrementally move to the new angle
        num_steps = max(1, num_steps)
        angle_inc: float = (angle - current_angle) / num_steps
        time_inc: float = time / (num_steps - 1)
        for n in range(num_steps):
            angle: float = current_angle + n * angle_inc
            self.write(index, angle)
            sleep(time_inc)

    def move_to_angles(self, servo_angles: list[tuple[int, float]], time: float | None = None, num_steps: int = 100) -> None:
        """Move the specified servo to the given logical angles in the given time (seconds)

        Args:
            servo_angles: list of tuples (index, logical angle) for each servo
            time (float): time (in seconds) to move between angles
            num_steps (int): number of steps to take in the movement
        """
        
        # Set starting angles for all servos
        for index, _ in servo_angles:
            self._servo_infos[index].angle = self.read(index)
            
        # Create time increment. Note: could be more sophisticated
        num_steps = max(1, num_steps)
        time_inc: float = time / (num_steps - 1)
        
        for n in range(num_steps, 0, -1):
            
            for index, angle_end in servo_angles:
                servo_info = self._servo_infos[index]
                
                angle_inc = (angle_end - servo_info.angle) / n
                new_angle: float = servo_info.angle + angle_inc
                
                self.write(index, new_angle)
                servo_info.angle = new_angle
                
                sleep(time_inc)
                
    def execute_gesture(self, gesture: Gesture, time: float, numsteps: int = 100, repeat: int = 1) -> None:
        """Execute the gesture over the given time, breaking it into numsteps. Optionally repeat the gesture
        for a given number of times.

        Args:
            gesture (Gesture): prescribed motion of the servos over time
            time (float): amount of time to execute the gesture in seconds
            numsteps (int, optional): Number of steps to execute, including start. Defaults to 100.
        """
        dt: float = time / numsteps
        indices: list[int] = gesture.indices
        
        for _ in range(repeat):
        
            # Loop over all time points
            for n in range(numsteps + 1):
                t_norm: float = n / numsteps
                angles: list[float] = gesture.get_angles(t_norm)

                # Loop over all servos
                t_start_us: float = ticks_us()
                for i in range(len(indices)):
                    index: int = indices[i]
                    self.write(index, angles[i])

                t_end_us: float = ticks_us()
                dt_elapsed: float = 1.0e-06*(t_end_us - t_start_us)
                sleep(max(0.0, dt - dt_elapsed))

    async def async_execute_gesture(self, gesture: Gesture, time: float, numsteps: int = 100, repeat: int = 1) -> None:
        """Execute the gesture over the given time, breaking it into numsteps

        Args:
            gesture (Gesture): prescribed motion of the servos over time
            time (float): amount of time to execute the gesture in seconds
            numsteps (int, optional): Number of steps to execute, including start. Defaults to 100.
        """
        dt: float = time / numsteps
        indices: list[int] = gesture.indices
        
        for _ in range(repeat):
        
            # Loop over all time points
            for n in range(numsteps + 1):
                t_norm: float = n / numsteps
                angles: list[float] = gesture.get_angles(t_norm)

                # Loop over all servos
                t_start_us: float = ticks_us()
                for i in range(len(indices)):
                    index: int = indices[i]
                    self.write(index, angles[i])

                t_end_us: float = ticks_us()
                dt_elapsed: float = 1.0e-06*(t_end_us - t_start_us)
                dt_wait: int = int(1000.0 * max(0.0, dt - dt_elapsed))
                await asyncio.sleep_ms(dt_wait)
    
    def _servo_angle_to_duty(self, servo_angle_deg: float) -> int:
        """Convert the servo angle to a duty cycle

        Args:
            servo_angle_deg (float): servo angle in deg to convert to a duty cycle

        Returns:
            int: duty cycle [0, 4095]
        """
        return int(self._offset + self._slope * servo_angle_deg)

    def _duty_to_servo_angle(self, duty: int) -> float:
        """Convert the duty cycle to an servo angle

        Args:
            duty (int): duty cycle [0, 4095] to convert to an angle

        Returns:
            float: servo angle in deg
        """
        return float(duty - self._offset) / self._slope
    
    def __str__(self) -> str:
        """String representation of the ServoList object."""
        servo_info_strs = f'ServoList: \n   {'\n   '.join(str(servo_info) for servo_info in self._servo_infos)}'
        return servo_info_strs
    

if __name__ == "__main__":
    # Create I2C object
    i2c = I2C(id=1, scl=Pin(15), sda=Pin(14))
    print(f'Found {len(i2c.scan())} i2c devices.')
    
    # Create servo info objects
    servo_infos =[
        ServoInfo(pin=15, index=0, servo_angle_0 = 107, sign = -1, name='lower-leg', angle_start=0, angle_end=90),
        ServoInfo(pin=14, index=1, servo_angle_0 = 20, sign = 1, name='upper-leg', angle_start=0, angle_end=90),
        ServoInfo(pin=13, index=2, servo_angle_0 = 125, sign = -1, name='shoulder', angle_start=-50, angle_end=50),
    ]
    for servo_info in servo_infos:
        print(servo_info)

    # Create ServoList object

    servo_list = ServoList(i2c, servo_infos)
    '''

    print('Moving to home position...', end='')
    servo_set.write(0, 30)
    servo_set.write(1, 30)
    servo_set.write(2, -45)
    print('done.')
    sleep(1)

    print('Starting walk gesture...', end='')
    walk_gesture: Gesture = Gesture(
            [
                [ 30,  40, 40, 40, 20,  20,  20,  30],
                [ 30,  40, 40, 40, 20,  20,  20,  30],
                [-45, -45, 00, 45, 45,  00, -45, -45]
            ]
    )
    asyncio.run(servo_set.async_execute_gesture(walk_gesture, time=2.0, numsteps=200, repeat=5))
    print('done.')

'''


