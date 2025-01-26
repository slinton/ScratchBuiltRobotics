#
# ServoBase
#
# Version 2025_01_25_01
#
# Note: this uses servo.py. That code could be included inside this class.
from servo import Servo
from time import sleep
import uasyncio as asyncio

class ServoBase:
    """This serves as a base class for servo control. A start and a end angle are provided. Note 
    that these angles are not necessarily in order. (angle_start may be > angle_end)
    Increasing angles are nevertheless defined to be moving from angle_start to angle_end, and
    decreasing angles are defined to be moving from angle_end to angle_start.
    """
    STOPPED = 'stopped'
    INCREASING = 'increasing'
    DECREASING = 'decreasing'

    def __init__(self, pin: int, angle_start: float, angle_end: float) -> None:
        self.servo = Servo(pin_id=pin)
        self.angle_start = angle_start
        self.angle_end = angle_end
        self.sign = 1 if angle_end > angle_start else -1
        self.angle_inc = 2 # degrees
        self.state = ServoBase.STOPPED


    def move_to_angle(self,  new_angle: float,  time: float | None = None, num_steps: int = 100) -> None:
        """Move to the given angle in the given time (seconds)

        Args:
            new_angle (float): angle to move to (deg)
            time (float): time (in seconds) to move between angles
            num_steps (int): number of steps to take in the movement
        """ 
        # Check to make sure the new_angle is within the limits
        if not self._angle_in_range(new_angle):
            raise ValueError('new_angle is not within the range of the servo')
        
        # Retrieve current angle
        current_angle = self.servo.read()
        #print(f'Current angle: {current_angle}')
            

        # Move in a single step to the new angle
        if current_angle == None or time == None or num_steps < 2:
            self.servo.write(new_angle)
            return

        # Move in multiple steps to the new angle
        angle_inc: float = (new_angle - current_angle) / (num_steps - 1)
        time_inc: float = time / (num_steps - 1)
        for i in range(num_steps):
            angle: float = current_angle + i * angle_inc
            #print(f'angle: {angle}')
            self.servo.write(angle)
            sleep(time_inc)

    def move_by(self, angle_inc: float) -> None:
        """Move the servo by the given angle increment

        Args:
            angle_inc (float): angle increment (deg)
        """
        current_angle = self.servo.read()
        
        if current_angle == None:
            raise ValueError('Unable to read current angle')

        new_angle = current_angle + angle_inc
        if self._angle_in_range(new_angle):
            self.servo.write(new_angle)


    def move_to_start(self, time: float = None) -> None:
        """Move to the start angle in the given time
        """
        self.move_to_angle(self.angle_start, time)
        
        
    def move_to_end(self, time: float = None) -> None:
        """Move to angle_end in the given time
        """
        self.move_to_angle(self.angle_end, time)

    def start_increasing(self, angle_inc: float = 2.0) -> None:
        """Used in conjunction with async run_loop to start moving
        the servo in the increasing direction. Note that the increasing
        direction is taken to be moving twoards angle_end, regardless of 
        whether angle_end is greater than angle_start or not.

        Args:
            angle_inc (float, optional): angle increment in degrees. Defaults to 2.0.
            This should always be positive.
        """
        if not self.state == ServoBase.INCREASING:
            print('start_increasing')
            self.state = ServoBase.INCREASING
            if angle_inc:
                self.angle_inc = angle_inc
        
    def stop(self) -> None:
        """Used in conjunction with async run_loop to stop movement
        """
        if not self.state == ServoBase.STOPPED:
            print('stop')
            self.state = ServoBase.STOPPED
        
    def start_decreasing(self, angle_inc: float = 2.0) -> None:
        """Used in conjunction with async run_loop to start moving
        the sero in the decreasing direction.  Note that the decreasing
        direction is taken to be moving twoards angle_start, regardless of 
        whether angle_start is less than angle_end or not.

        Args:
            angle_inc (float, optional): angle increment in degrees. Defaults to 2.0.
            This should always be positive.
        """
        if not self.state == ServoBase.DECREASING:
            print('start_decreasing')
            self.state = ServoBase.DECREASING
            if angle_inc:
                self.angle_inc = angle_inc
    
    async def run_loop(self)-> None:
        """Async loop to run the servo movement. The assumption is some other 
        code will set the state to INCREASING, STOPPED, or DECREASING
        """
        while True:
            try:
                while self.state == ServoBase.INCREASING:
                    self.move_by(self.sign * self.angle_inc)
                    await asyncio.sleep_ms(10)
              
                while self.state == ServoBase.DECREASING:
                    self.move_by(-self.sign * self.angle_inc)
                    await asyncio.sleep_ms(10)

                if self.state == ServoBase.STOPPED:
                    await asyncio.sleep_ms(10)
                    
            except Exception as e:
                print(f'Exception: {e}')
                self.state = ServoBase.STOPPED


    def _angle_in_range(self, angle: float) -> bool:
        """Check if the angle is within the range of the servo

        Args:
            angle (float): angle to check

        Returns:
            bool: True if the angle is within the range
        """
        return (self.angle_end - angle) * (angle - self.angle_start) >= 0
    

if __name__ == '__main__':
    servo = ServoBase(pin=16, angle_start=0, angle_end=180)
    servo.move_to_start()
    sleep(0.5)
        
    servo.move_to_end()
    sleep(0.5)
        
    servo.move_to_start(time=2)
    sleep(0.5)
        
    servo.move_to_end(time=2)
    sleep(0.5)
        
