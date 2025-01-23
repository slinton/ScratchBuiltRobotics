#
# Lifter
#
# Version 25_01_20_01
#
#
#
from servo import Servo
from time import sleep
import uasyncio as asyncio

# TODO: use an enum for the state?
# Is the use of the two types of angles worth the trouble?

class Lifter:
    """Implement the gripper lifter mechanism
    """
    STOPPED = 'stopped'
    LIFTING = 'lifting'
    LOWERING = 'lowering'

    def __init__(self,
                 pin: int=16,
                 servo_top_angle: float = 0.0,
                 servo_bottom_angle: float=180.0,
                 ) -> None:
        """Initializer

        Gripper lifter angle goes from 0 (closed) to open_angle (fully open)
        These angles correspond with the servo_top_angle and servo_bottom_angle, respectively

        Args:
            pin (int, optional): pin for the gripper PWM signal. Defaults to 16.
            open_angle (float, optional): Angle in degrees corresponding to open gripper. Defaults to 160.0.
            close_angle (float, optional): Angle in degrees corresponding to closed gripper. Defaults to 70.0.
        """
        self.servo: Servo = Servo(pin_id=pin)
        self.servo_top_angle: float = servo_top_angle
        self.servo_bottom_angle: float = servo_bottom_angle
        self.top_angle: float = 0.0
        self.bottom_angle: float = abs(self.servo_bottom_angle - self.servo_top_angle)
        self.sign: float = 1 if self.servo_bottom_angle > self.servo_top_angle else -1
        self.angle: float | None = None
        
        self.state = Lifter.STOPPED
        
    def start_lift(self) -> None:
        if not self.state == Lifter.LIFTING:
            print('start_lift')
            self.state = Lifter.LIFTING
        
    def stop(self) -> None:
        if not self.state == Lifter.STOPPED:
            print('stop')
            self.state = Lifter.STOPPED
        
    def start_lower(self) -> None:
        if not self.state == Lifter.LOWERING:
            print('stop')
            self.state = Lifter.LOWERING
        
    def lift(self, time: float = None) -> None:
        """Move gripper to the top
        """
        if time == None or self.angle == None:
            self.set_angle(self.top_angle)
        else:
            self.move(self.angle, self.top_angle, time)
        
        
    def lower(self, time: float = None) -> None:
        """Move gripper to the bottom
        """
        if time == None or self.angle == None:
            self.set_angle(self.bottom_angle)
        else:
            self.move(self.angle, self.bottom_angle, time)
            
    def move_by(self, d_angle: float) -> None:
        """Move the gripper by the angle increment given. Lower direction is +

        Args:
            d_angle (float): requested change in angle (degrees)
        """
        if self.angle == None: return
        
        new_angle = self.angle + d_angle
        if self.top_angle < new_angle < self.bottom_angle:
            self.set_angle(new_angle)

    def move_to(self, end_angle: float, time: float, num_angles: int = 100):
        """Move from the current angle to the end angle (in degrees) in the given amount of
        time (in seconds). 

        Args:
            end_angle (float): Ending angle of the motion, degrees
            time (float): time in which to make the motion, in seconds
            num_angles (int, optional): Number of steps to take. Defaults to 100.
        """
        self._move(self.angle, end_angle, time, num_angles)
        
    def _move(self, start_angle: float, end_angle: float, time: float, num_angles: int = 100):
        """Move from the start angle to the end angle (in degrees) in the given amount of
        time (in seconds). 
        Caution: if the start_angle is not the current angle, this will start with an abrupt
        movement to the start_angle

        Args:
            start_angle (float): Starting angle of the motion, degrees
            end_angle (float): Ending angle of the motion, degrees
            time (float): time in which to make the motion, in seconds
            num_angles (int, optional): Number of steps to take. Defaults to 10.
        """
        d_angle: float = (end_angle - start_angle) / (num_angles - 1)
        d_time: float = time / (num_angles - 1)
    
        for i in range(num_angles):
            angle: float = start_angle + i * d_angle
            print(angle)
            self.set_angle(angle)
            sleep(d_time)

    def get_angle(self) -> float:
        """Get current angle in degrees. This will be None when starting out.

        Returns:
            float: current angle in degrees
        """
        return self.angle
        
    def set_angle(self, angle: float) -> None:
        """Set angle of gripper. O represents closed. All other methods should call
        this one.

        Args:
            angle (float): angle of gripper. 
        """
        servo_angle: float = self.servo_top_angle + self.sign * angle
        self._set_servo_angle(servo_angle=servo_angle)
        self.angle = angle
        
    def _set_servo_angle(self, servo_angle: float) -> None:
        """Helper function to set servo angle based. This actually moves the servo

        Args:
            servo_angle (float): servo angle in degrees
        """
        servo_angle: float = self._clamp(servo_angle, self.servo_bottom_angle, self.servo_top_angle)
        print(f'Lifter servo angle = {servo_angle:.0f}')
        self.servo.write(servo_angle)
        
    def _clamp(self, value: float, start: float, end: float) -> float:
        """Return value clamped between the other two values"""
        min_value = min(value, min(start, end))
        max_value = max(value, max(start, end))
        return min(max_value, max(min_value, value))
    
    async def run_loop(self)-> None:
        while True:
            try:
                while self.state == Lifter.LIFTING:
                    self.move_by(-2)
                    await asyncio.sleep_ms(10)
                
                while self.state == Lifter.LOWERING:
                    self.move_by(2)
                    await asyncio.sleep_ms(10)

                if self.state == Lifter.STOPPED:
                    await asyncio.sleep_ms(10)
                    
            except Exception as e:
                print(f'Exception: {e}')
                self.state = Lifter.STOPPED
        
if __name__ == '__main__':
    lifter = Lifter()
    lifter.lift()
    sleep(0.5)
    lifter.lower()
    sleep(0.5)
    lifter.lift()
    
    
#     for _ in range(5):
#         gripper.open()
#         sleep(1)
#         gripper.close()
#         sleep(1)
#     gripper.open()
#     sleep(2)

#     num_angles: int = 100
#     max_angle: float = 90.0
#     time: float = 3.0
#     d_angle: float = max_angle / (num_angles-1)
#     print(f'd_angle = {d_angle}')
#     d_time: float = time / (num_angles-1)
#     
#     for i in range(num_angles):
#         angle: float = i * d_angle
#         print(angle)
#         gripper.set_angle(angle)
#         sleep(d_time)
        
    


