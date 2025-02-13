#
# ServoSet
#
# V2025_02_12_01
#
import ustruct
from math import radians
from machine import I2C
from time import sleep, sleep_us
from servo_info import ServoInfo

class ServoSet:
    """Uses the PCA9685 to control a set of servos.
    """

    def __init__(self, 
                 i2c: I2C, 
                 servo_infos,
                 address: int = 0x40, 
                 freq: float = 50, 
                 min_us: float = 600.0, # 544
                 max_us: float = 2400.0,
                 max_angle_deg: float = 180.0) -> None:
        """_summary_

        Args:
            i2c I2C: I2C object
            servo_infos (List[ServoInfo]): list of servo info objects
        """
        self._i2c: I2C = i2c
        self._servo_infos = servo_infos
        self._address: int = address

        # Compute min and max duty cycles (0-4095)
        t_period_us: int = 1_000_000 / freq # period in us
        min_duty: float = self._us2duty(min_us, t_period_us)
        max_duty: float = self._us2duty(max_us, t_period_us)

        # Slope and offset for converting angles (degrees) to duty cycles [0, 4095]
        self._slope: float = (max_duty - min_duty) / max_angle_deg
        self._offset: float = min_duty

        self.reset()
        self.set_freq(freq)
        
        # Set all servo angles
        for servo_info in self._servo_infos:
            servo_info.angle = self.read(servo_info.index)
            print(f'{servo_info}')
            
    def _us2duty(self, t_us: float, t_period_us: float) -> int:
        return int(4095 * t_us / t_period_us)

    def reset(self) -> None:
        self._write(0x00, 0x00) # Mode1
        
    def set_freq(self, freq=None):
        if freq is None:
            return int(25000000.0 / 4096 / (self._read(0xfe) - 0.5))
        prescale = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode = self._read(0x00) # Mode 1
        self._write(0x00, (old_mode & 0x7F) | 0x10) # Mode 1, sleep
        self._write(0xfe, prescale) # Prescale
        self._write(0x00, old_mode) # Mode 1
        sleep_us(5)
        self._write(0x00, old_mode | 0xa1) # Mode 1, autoincrement on
        
    def _write(self, address, value):
        self._i2c.writeto_mem(self._address, address, bytearray([value]))

    def _read(self, address):
        return self._i2c.readfrom_mem(self._address, address, 1)[0]
        
    def write(self, index: int, angle: float) -> None:
        """Write the angle to the servo

        Args:
            index (int): index of the servo
            angle (float): angle to write to the servo
        """
        # Find duty cycle from angle
        duty = self._angle_to_duty(angle)
        address = 0x06 + 4 * index
        
        # Create data to write to I2C
        data = ustruct.pack('<HH', 0, duty)
        self._i2c.writeto_mem(self._address, address,  data)

    def read(self, index: int) -> float:
        """Read the angle from the servo

        Args:
            index (int): index of the servo

        Returns:
            float: angle of the servo
        """
        # Read the duty cycle from the servo
        address = 0x06 + 4 * index
        data = self._i2c.readfrom_mem(self._address, address, 4)
        duty = ustruct.unpack('<HH', data)[1]
        angle = self._duty_to_angle(duty)
        return angle

    def move_to_angle(self, index: int, angle: float, time: float | None = None, num_steps: int | None = None) -> None:
        """Move the specified servo to the given angle in the given time (seconds)

        Args:
            index (int) servo index
            angle (float) angle to move to in degrees
            time (float): time (in seconds) to move between angles
            num_steps (int): number of steps to take in the movement
        """ 
        # Loop over all requested angle values
        servo_info = self._servo_infos[index]

        # Check to make sure the new_angle is within the limits
        if not servo_info.angle_in_range(angle):
            raise ValueError('new_angle is not within the range of the servo')
            
        # Retrieve current angle
        current_angle = self.read(index)
        
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


    def move_to_angles(self, servo_angles, time: float | None = None, num_steps: int = 100) -> None:
        """Move the specified servo to the given angle in the given time (seconds)

        Args:
            servo_angles list of tuples with index, angle values
            index (int) servo index
            angle (float) angle to move to in degrees
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
    from time import sleep

    # Create I2C object
    i2c = I2C(0, sda=0, scl=1)
    print(f'Found {len(i2c.scan())} i2c devices.')
    
    # Create servo info objects
    servo_infos = [ServoInfo(0, 0, 180), ServoInfo(1, 0, 180)]
    for servo_info in servo_infos:
        print(servo_info)

    # Create ServoSet object
    servo_set = ServoSet(i2c, servo_infos)
    
    servo_set.write(0, 10)
    print(servo_set.read(0))
    sleep(1)
    
    servo_set.write(0, 170)
    sleep(1)
    print(servo_set.read(0))
    
    servo_set.write(0, 10)
    print(servo_set.read(0))
    sleep(1)

    # Move servos to angles
    servo_set.move_to_angle(0, 170, time=4.0)
    sleep(2)
    
    t = 0.5
    servo_set.move_to_angles([(0, 170), (1, 120)], time=t)
    servo_set.move_to_angles([(0, 40), (1, 80)], time=t)
    servo_set.move_to_angles([(0, 170), (1, 120)], time=t)
    servo_set.move_to_angles([(0, 40), (1, 80)], time=1.0)
